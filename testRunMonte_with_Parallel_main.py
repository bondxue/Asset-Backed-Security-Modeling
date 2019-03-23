'''
Purpose: This program is to test RunMonte() with runSimulationParallel()
Author: Mengheng
Date: 12/05/2018
'''

import csv
from loan.loan_pool import LoanPool
from loan.autoloan import AutoLoan
from asset.car_base import Car
from tranche.structured_securities import StructuredSecurities
from usefulFunctions.doWaterfall import doWaterfall
import itertools
from simulation.runSimulation import runSimlutation
import numpy as np
from simulation.runMonte import runMonte
from tranche.tranche_base import Tranche
from usefulFunctions.timer import Timer


def main():
    # logging.basicConfig(level=logging.INFO)
    # create a loan_pool object by loading the loan data in the csv file
    loan_pool = LoanPool([])
    with open('Loans.csv',
              'r') as fp:
        reader = csv.reader(fp, delimiter=',')
        header = next(reader, None)  # skip first row
        for row in reader:
            asset_type = row[5]
            asset_value = float(row[6])
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
    tranche_percents = [0.8, 0.4]
    tranche_rates = [0.02, 0.03]  # subordinated tranche should have higher rate since increased risk
    tranche_levels = [0, 1]  # 0 is higher class than 1
    coeffs = [1.2, 0.8]
    tolerance = 0.01
    NSIM = 60
    num_processes = 20
    with Timer('MC time cost'):
        MC_matrics = runMonte(loan_pool, tranche_percents, tranche_rates, tranche_levels, coeffs, tolerance, NSIM, num_processes)

    # DIRR, WAL, rate, Rating of each tranche
    print '{0:<20s} {1:<20s} {2:<20s} {3:<20s}'.format('DIRR', 'AL', 'rate', 'LetterRating')
    for matric in MC_matrics:
        print '{0:s}   {1:s}    {2:s}    {3:s}'.format(*matric)

    '''
    since my MC is extremely very slow, I only test relatively small NSIM 
    when NSIM = 60:
    num_processes = 10   MC time cost: 131.306999922 s
    num_processes = 20   MC time cost: 118.375 s  
    num_processes = 30   MC time cost: 114.0849998 s
    In this case, num_processes = 30  is the best choice.
    when NSIM = 80:
    num_processes = 20   MC time cost: 135.541999817 s
    The optimal process number is also dependent on NSIM. 
    '''


if __name__ == '__main__':
    main()
