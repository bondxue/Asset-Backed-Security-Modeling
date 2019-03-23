'''
Purpose: This program is to do waterfall for both loan_pool and structured securities and save results in csv files
Author: Mengheng
Date: 11/26/2018
'''

import csv
from loan.loan_pool import LoanPool
from loan.autoloan import AutoLoan
from asset.car_base import Car
from tranche.structured_securities import StructuredSecurities
from usefulFunctions.doWaterfall import doWaterfall
import itertools


def main():
    # logging.basicConfig(level=logging.INFO)
    # create a loan_pool object by loading the loan data in the csv file
    loan_pool = LoanPool([])
    with open('Loans.csv', 'r') as fp:
        reader = csv.reader(fp, delimiter=',')
        header = next(reader, None)  # skip first row
        for row in reader:
            asset_type = row[5]
            asset_value = row[6]
            if asset_type == 'Car':  # in the csv file we only have car type asset
                car = Car(asset_value)
                loan_type = row[1]
                face = float(row[2])
                rate = float(row[3])
                term = int(row[4])
                if loan_type == 'Auto Loan':  # in the cvs file we only have auto loan type
                    loan = AutoLoan(term, rate, face, car)  # create loan object
                    loan_pool.loan_list.append(loan)  # add it to loan_pool

        # set tranche A and tranche B information
        tranche_percents = [0.3, 0.7]
        tranche_rates = [0.02, 0.05]  # subordinated tranche should have higher rate since increased risk
        tranche_levels = [0, 1]  # 0 is higher class than 1
        structured_securities = StructuredSecurities.constructSecurities(loan_pool.totalPrincipal(), tranche_percents,
                                                                         tranche_rates, tranche_levels)
        structured_securities.mode = 'Sequential'  # set mode Sequential or Pro Rata
        loan_pool_waterfall, structured_securities_waterfall, reserve_amount = doWaterfall(loan_pool,
                                                                                           structured_securities)

        with open('loan pool waterfall.csv', 'w') as lp_fp:
            header_list = []
            # add header line for each loan
            for i in range(len(loan_pool_waterfall[0])):
                header = ['Loan ' + str(i + 1) + ' Monthly Payment', 'Loan ' + str(i + 1) + ' Principal Due',
                          'Loan ' + str(i + 1) + ' Interest Due', 'Loan ' + str(i + 1) + ' Balance']
                header_list.append(header)
            flattened_headers = [item for sublist in header_list for item in sublist]
            lp_fp.write(','.join(map(str, list(flattened_headers))) + '\n')

            # do loan waterfall and save results in one csv file
            for loans in loan_pool_waterfall:
                # since it is list of list, we need to flatten it first
                flattened_loans = [item for sublist in loans for item in sublist]
                lp_fp.write(','.join(map(str, list(itertools.chain(flattened_loans)))) + '\n')

        with open('securities_waterfall.csv', 'w') as sc_fp:
            header_list = []
            # add header for each structured security
            for i in range(len(structured_securities_waterfall[0])):
                header = ['Tranche ' + str(i + 1) + ' Interest Due', 'Tranche ' + str(i + 1) + ' Interest Paid',
                          'Tranche ' + str(i + 1) + ' Interest Shortfall', ' Tranche ' + str(i + 1) + ' Principal Paid',
                          'Tranche ' + str(i + 1) + ' Balance']
                header_list.append(header)
            header_list.append(['Reserve Account'])
            flattened_headers = [item for sublist in header_list for item in sublist]
            sc_fp.write(','.join(map(str, list(flattened_headers))) + '\n')

            # do securities waterfall and save results in one csv file
            for tranches, res_cash in zip(structured_securities_waterfall, reserve_amount):
                flattened_tranches = [item for sublist in tranches for item in sublist]  # flatten the list first
                sc_fp.write(','.join(map(str, list(itertools.chain(flattened_tranches))) +
                                     [str(res_cash)]) + '\n')

        '''
        Each tranche's balance get successfully paid down to 0, and there is no money left in the 
        reserve account at the end. 
        '''


if __name__ == '__main__':
    main()
