'''
3.3.4
Purpose: This module contains classes related to Mortgages.
update: 10/31/2018   __init__ raise exception instead of print error message
        11/22/2018   replace term with start_date, end_date
        11/25/2018   change back to term

Author: Mengheng
Date: 10/31/2018
'''
from loans import VariableRateLoan, FixedRateLoan
from asset.house_base import HouseBase
import logging


# MortgageMixin class which contains mortgage-specific methods
class MortgageMixin(object):
    # save home parameter as an HouseBase object,
    # if not, print an error message and leave the function
    def __init__(self, term, rate, face, home):
        if not isinstance(home, HouseBase):
            logging.error('input {} is not HomeBase object.'.format(home))
            raise TypeError('Home parameter should be HouseBase object.')
        super(MortgageMixin, self).__init__(term, rate, face, home)

    # Mortgage-specific functionality
    # function to return private mortgage insurance
    def PMI(self, period=1):
        LTV = self._face * 1.0 / self._asset._val  # loan to value ratio
        return 0.000075 * self._face if LTV < 0.8 else 0

    # override base class monthlyPayment function
    def monthlyPayment(self, period=1):
        return super(MortgageMixin, self).monthlyPayment(period) + self.PMI(period)

    # override base class principleDue function
    def principleDue(self, period):
        return self.monthlyPayment(period) - self.interestDue_formula(period)


# VariableMortgage derived from both MortgageMixin and VariableRateLoan
# make sure to derive-from mixin class first, to ensure its version of monthlyPmt takes precedence
class VariableMortgage(MortgageMixin, VariableRateLoan):
    def __init__(self, term, rateDict, face, home):
        super(VariableMortgage, self).__init__(term, rateDict, face, home)


# FixedMortgage derived from both MortgageMixin and FixedRateLoan
class FixedMortgage(MortgageMixin, FixedRateLoan):
    def __init__(self, term, rate, face, home):
        super(FixedMortgage, self).__init__(term, rate, face, home)
