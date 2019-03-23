'''
Purpose: This module contain the Loan base class
update: 10/31/2018   __init__ raise exception instead of print error message
        11/01/2018   add debug-level log to totalInterest() and principalDue_formula() functions
                     add error-level log in __init__() for wrong type input parameter
                     add info-level log in all functions with period parameter, if period>term, then display the error message
                     add warn-level log in the recursive versions of waterfall functions
        11/22/2018   replace term with start_date, end_date
                     add term method to calculate and return loan term from start_date and end_date
        11/22/2018   modify interestDue_recursive() function with memoize decorator
        11/25/2018   change back to term instead of start_date, end_date
        11/26/2018   add checkDefault() function
                     add class level lists to determine probability of default of a loan for a given time period
                     add defaulted object variable
                     modify all the balance, face, monthly payment functions to consider default loans
        12/05/2018   add reset() method for monte carlo simulation
Author: Mengheng
Date: 10/31/2018
'''
from asset.asset import Asset
import logging
from usefulFunctions.memoize import Memoize
import numpy as np


class Loan(object):
    def __init__(self, term, rate, face, asset):
        # save asset parameter as an Asset object,
        # if not, print an error message and leave the function
        if not isinstance(asset, Asset):
            logging.error('input {} is not Asset object.'.format(asset))
            raise TypeError('Asset parameter should be an Asset object.')
        # self._start_date = start_date
        # self._end_date = end_date
        self._term = term
        self._rate = rate
        self._face = face
        self._asset = asset
        self._defaulted = False

    # getter/ setter property functions
    @property
    def term(self):
        return self._term

    # @property
    # def start_date(self):
    #     return self._start_date
    #
    # @property
    # def end_date(self):
    #     return self._end_date

    @property
    def defaulted(self):
        return self._defaulted

    @defaulted.setter
    def defaulted(self, idefault):
        self._defaulted = idefault

    @property
    def rate(self):
        return self._rate

    @property
    def face(self):
        return 0 if self.defaulted else self._face  # if loan defaulted face = 0

    @property
    def asset(self):
        return self._asset

    @term.setter
    def term(self, iterm):
        self._term = iterm

    # @start_date.setter
    # def start_date(self, istart_date):
    #     #     self._start_date = istart_date
    #     #
    #     # @end_date.setter
    #     # def end_date(self, iend_date):
    #     #     self._end_date = iend_date

    @rate.setter
    def rate(self, irate):
        self._rate = irate

    @face.setter
    def face(self, iface):
        self._face = iface

    @asset.setter
    def asset(self, iasset):
        self._asset = iasset

    def rate(self, period):
        # should be overriden by derived class, this function makes Loan class abstract
        raise NotImplementedError()

    # # term function to calculate and return loan term from start and end dates
    # def term(self):
    #     return (self._end_date - self._start_date).days / 30

    # function to return monthly payment
    # add period as dummy parameter, set default value = 1
    def monthlyPayment(self, period=1):
        # if loan defaulted, monthly payment = 0
        return 0 if self._defaulted else self._rate * self._face / (1 - (1 + self._rate) ** (-self._term))

    # function to return total payment
    def totalPayments(self):
        return sum([self.monthlyPayment(period) for period in range(self._term)])

    # function to return total interest
    def totalInterest(self):
        logging.debug('total payment = {}'.format(
            self.totalPayments()))  # debug-level log, just show interim step:  total payment
        logging.debug('face = {}'.format(self._face))  # debug-level log, just show interim step: face value
        logging.debug('total interest = {}'.format(self.totalPayments() - self._face))

        return self.totalPayments() - self._face

    # interest due using formula version
    def interestDue_formula(self, period):
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
        else:
            if period < 1:  # if period is 0, interest due is 0
                return 0
            return self.balance_formula(period - 1) * self._rate

    # interest due using recursive version
    @Memoize
    def interestDue_recursive(self, period):
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
        else:
            if period < 1:  # if period is 0, no interest due
                return 0
            elif period < 2:  # if period is 1, return face * rate
                logging.warn(
                    'You are using recursive version of interestDue function, which will take so long. Not recommended! Please use interestDue_formula() instead.')
                return self._face * self._rate
            else:
                return (1 + self._rate) * self.interestDue_recursive(period - 1) - self.monthlyPayment(
                    period) * self._rate

    # principal due using formula version
    def principalDue_formula(self, period):
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
        else:
            logging.debug('monthly payment in the {n}th months = {m}'.format(m=self.monthlyPayment(period), n=period))
            logging.debug('interest due in the {n}th month = {i}'.format(n=period, i=self.interestDue_formula(period)))
            logging.debug('principal due in the {n}th month = {p}'.format(n=period, p=self.monthlyPayment(
                period) - self.interestDue_formula(period)))
            return self.monthlyPayment(period) - self.interestDue_formula(period)

    # principal due using recursive version
    def principalDue_recursive(self, period):
        logging.warn(
            'You are using recursive version of principalDue function, which will take so long. Not recommended! Please use principalDue_formula() instead.')
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
        else:
            if period < 1:  # if period is 0, no principal due
                return 0
            else:
                return (1 + self._rate) * self.principalDue_formula(period - 1)

    # outstanding balance using formula version
    def balance_formula(self, period):
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
        else:
            # if loan defaulted, balance = 0
            return 0 if self._defaulted else self._face * (1 + self._rate) ** period - self.monthlyPayment(period) * (
                    ((1 + self._rate) ** period - 1) / self._rate)

    # outstanding balance using recursive version
    def balance_recursive(self, period):
        if not self._defaulted:
            if period > self._term:
                logging.info(
                    'period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
            else:
                if period < 1:  # if period is 0, return the initial face value
                    logging.warn(
                        'You are using recursive version of balance function, which will take so long. Not recommended! Please use balance_formual() instead.')
                    return self._face
                else:
                    return (1 + self._rate) * self.balance_recursive(period - 1) - self.monthlyPayment(period)
        else:
            return 0

    # class level function to return monthly payment
    @classmethod
    def calcMonthlyPmt(cls, face, rate, term):
        return rate * face / (1 - (1 + rate) ** (-term))

    # class level function to return balance
    @classmethod
    def calcBalance(cls, face, rate, term, period):
        if period > term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=term))
        else:
            return face * (1 + rate) ** period - cls.calcMonthlyPmt(face, rate, term) * (
                    ((1 + rate) ** period - 1) / rate)

    # modified monthly payment function to delegate to the class-level function
    def monthlyPayment_modified(self, period=1):
        return 0 if self._defaulted else self.calcMonthlyPmt(self._face, self._rate, self._term)

    # modified balance function to delegate to the class-level function
    def balance_modified(self, period):
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
        else:
            return 0 if self._defaulted else self.calcBalance(self._face, self._rate, self._term, period)

    # static-level function to convert annual rate to monthly rate
    @staticmethod
    def monthlyRate(annual_rate):
        return annual_rate / 12.0

    # static-level function to convert monthly rate to annual rate
    @staticmethod
    def annualRate(monthly_rate):
        return monthly_rate * 12.0

    # method to return current asset value for the given period times a recovery multiplier
    def recoveryValue(self, period):
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
            return 0
        else:
            return self._asset.current_val(period) * 0.6  # recovery multiplier is 0.6

    # method to return available equity (current value - balance)
    def equity(self, period):
        if period > self._term:
            logging.info('period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
        else:
            return self.asset.current_val(period) - self.balance_formula(period)

    # class level lists to determine probability of default of a loan for a given time period
    default_time_periods = np.array([1, 10, 60, 120, 180, 210, 360])
    default_probabilities = [0.0005, 0.001, 0.002, 0.004, 0.002, 0.001]

    # check default function
    def checkDefault(self, default_flag):
        if default_flag == 0:  # 0: default 1: not default
            self._defaulted = True  # update defaulted status

    # reset function
    def reset(self):
        self._defaulted = False
