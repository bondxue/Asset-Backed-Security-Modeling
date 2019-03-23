'''
Purpose: This module contains the LoanPool class
Update: 10/29/208 make it iterable
        11/25/2018 add getWaterfall function
        11/26/2018 add checkDefaults() function
        12/05/2018 add reset() method for monte carlo simulation
Author: Mengheng
Date: 10/29/2018
'''

import numpy as np
from loan_base import Loan


class LoanPool(object):
    def __init__(self, loan_list):
        self._loan_list = loan_list

    @property
    def loan_list(self):
        return self._loan_list

    # method to get total loan principal
    def totalPrincipal(self):
        return sum(loan._face for loan in self._loan_list)

    # method to get total loan balance for a given period
    def totalBalance(self, period):
        return sum(loan.balance_formula(period) for loan in self._loan_list)

    # method to get aggregate principal due in a given period
    def totalPrincipalDue(self, period):
        return sum(loan.principalDue_formula(period) for loan in self._loan_list)

    # method to get aggregate interest in a given period
    def totalInterestDue(self, period):
        return sum(loan.interestDue_formula(period) for loan in self._loan_list)

    # method to get aggregate total payment in a given period
    def totalPaymentDue(self, period):
        return sum(loan.monthlyPayment(period) for loan in self._loan_list)

    # method to return number of active loan
    # active loans have balances greater than 0
    def numOfActive(self, period):
        return len([loan for loan in self._loan_list if loan.balance_formula(period) > 0])

    # method to compute WAR
    def WAR(self):
        numerator = sum(loan._face * loan._rate for loan in self._loan_list)
        denominator = sum(loan._face for loan in self._loan_list)
        return numerator / denominator

    # method to computer WAM
    def WAM(self):
        numerator = sum(loan._face * loan._term * 1.0 for loan in self._loan_list)
        denominator = sum(loan._face for loan in self._loan_list)
        return numerator / denominator

    # 3.1.2.c
    # function to compute WAM with reduce()
    def WAM_reduce(self):
        term_list = [loan._term for loan in self._loan_list]  # create a list of term
        face_list = [loan._face for loan in self._loan_list]  # crate a list of amount
        return reduce(fn, zip(face_list, term_list), 0) / sum(face_list)

    # function to compute WAR with reduce()
    def WAR_reduce(self):
        rate_list = [loan._rate for loan in self._loan_list]  # create a list of rate
        face_list = [loan._face for loan in self._loan_list]  # crate a list of amount
        return reduce(lambda total, (face, rate): total + face * rate, zip(face_list, rate_list), 0) / sum(
            face_list)

    # using __iter__ method to make LoanPool class iterable
    def __iter__(self):
        return iter(self._loan_list)

    # getwaterfall function
    def getWaterfall(self, period):
        res = []
        for loan in self._loan_list:
            res.append(
                [loan.monthlyPayment(period), loan.principalDue_formula(period), loan.interestDue_formula(period),
                 loan.balance_formula(period)])
        return res

    # check defaults function
    def checkDefaults(self, period):
        # unify the time period in a certain time period have the same interval index
        default_prob_index = np.where(period <= Loan.default_time_periods)[0][0]
        # obtain default prob for that certain period
        default_prob = Loan.default_probabilities[default_prob_index]
        # instead create uniform random integers for each loan, I just generate a uniform distribution
        # probability for each loan and check whether the probability is smaller than the default probability
        # if it is, return 0 indicating default happens, 1 otherwise.
        default_list = np.asarray(np.random.uniform(size=len(self._loan_list)) > default_prob, dtype=int)
        recovery_value = 0
        for loan, default_flag in zip(self._loan_list, default_list):
            if not loan.defaulted:  # check only when defaulted flag is false
                loan.checkDefault(default_flag)  # update the loan default status
                if loan.defaulted:  # if loan is default, return the recovery value of the asset
                    recovery_value += loan.recoveryValue(period)
        return recovery_value  # return all the defaulted loan's asset recovery value

    # reset function
    def reset(self):
        for loan in self._loan_list:
            loan.reset()


# global function as callable in WAM_reduce()
def fn(total, (face, term)):
    return total + face * term * 1.0
