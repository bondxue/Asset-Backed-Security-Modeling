'''
Purpose: This program is to create structured securities class
Author: Mengheng
Date: 11/23/2018
'''

from tranche_base import Tranche
from standard_tranche import StandardTranche
import logging


class StructuredSecurities(object):
    def __init__(self, total_notional):
        self._total_national = total_notional
        self._tranche_list = []
        self._mode = 'Pro Rata'  # default mode is Pro Rata
        self._reserve_account = 0

    @property
    def reserve_amount(self):
        return self._reserve_account

    @property
    def tranche_list(self):
        return self._tranche_list

    @property
    def mode(self):
        return self._mode

    # function to add a tranche in to structured security
    def addTranche(self, notional_percent, rate, subordination_level):
        # instantiate a new tranche
        new_tranche = StandardTranche(self._total_national * notional_percent, notional_percent, rate,
                                      subordination_level)
        # add tranche to the list
        self._tranche_list.append(new_tranche)
        self._tranche_list = sorted(self._tranche_list, key=lambda x: x.subordination_level)

    # class function that create StructuredSecurities object
    @classmethod
    def constructSecurities(cls, total_notional, notional_percents, rates, subordination_levels):
        structured_securities = StructuredSecurities(total_notional)
        for notional_percent, rate, subordination_level in zip(notional_percents, rates, subordination_levels):
            structured_securities.addTranche(notional_percent, rate, subordination_level)
        return structured_securities

    # set mode 'Sequential' or 'Pro Rata'
    @mode.setter
    def mode(self, imode):
        if imode not in {'Sequential', 'Pro Rata'}:
            logging.error('invalid mode. (Sequential / Pro Rata)')
        self._mode = imode

    # function to increase current time period of each tranche in structured security
    def increaseTimePeriod(self):
        for tranche in self._tranche_list:
            tranche.increaseTimePeriod()

    def makePayments(self, cash_amount):
        cash_left = cash_amount + self._reserve_account  # reserve account is added to cash amount
        self._reserve_account = 0  # reset reserve account to 0
        # make interest payment to each tranche first
        for tranche in self._tranche_list:
            if tranche.current_notional_balance > 0:
                cash_left = tranche.makeInterestPayment(cash_left)
        # make principal payment second
        if cash_left > 0:
            if self._mode == 'Sequential':
                for tranche in self._tranche_list:
                    if tranche.current_notional_balance > 0 and cash_left > 0:
                        cash_left = tranche.makePrincipalPayment(cash_left)
            elif self._mode == 'Pro Rata':
                temp_cash_left = 0
                for tranche in self._tranche_list:
                    if tranche.current_notional_balance > 0:
                        # never overpay tranche balance, keep the extra cash
                        temp_cash_left += tranche.makePrincipalPayment(tranche.notional_percent * cash_left)
                cash_left = temp_cash_left
        # if there exist at least one tranche which are not fully paid, we will update the reserve account
        for tranche in self._tranche_list:
            if tranche.current_notional_balance > 0:
                self._reserve_account = cash_left

    # function return tranche information for waterfall
    def getWaterfall(self):
        res = [[] for tranche in self._tranche_list]  # list of tranche
        for i, tranche in enumerate(self._tranche_list):
            interest_due = tranche.interestDue
            interest_paid = tranche.interestPaid
            interest_shortfall = tranche.interestShortfall
            principal_paid = tranche.principalPaid
            balance = tranche.current_notional_balance
            res[i] = [interest_due, interest_paid, interest_shortfall, principal_paid, balance]
        return res

    def reset(self):
        self._reserve_account = 0
        for tranche in self._tranche_list:
            tranche.reset()
