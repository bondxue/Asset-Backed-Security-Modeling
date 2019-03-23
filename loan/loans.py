'''
Purpose: This module contains derived Loan classes.
Update: 11/22/2018   replace term with start_date, end_date
        11/25/2018   change back to term
Author: Mengheng
Date: 10/24/2018
'''
from loan_base import Loan


# fixed rate loan class derived from Loan class
class FixedRateLoan(Loan):
    def rate(self, period):
        # overrides the base class
        return self._rate  # self._rate defined in the base class


# variable rate Loan class derived from Loan class
class VariableRateLoan(Loan):
    def __init__(self, term, rateDict, face, asset):
        self._rateDict = rateDict
        # invoke the initialization function in the base class
        # put None for rate parameter since we don't need it here
        super(VariableRateLoan, self).__init__(term, None, face, asset)

    def rate(self, period):
        # add code to find the rate for a given period.
        # rateDict contains startPeriod as key and rate as value,
        # for each rate.
        # use rate to store the current rate, initialize it with initial rate
        rate = self._rateDict[min(self._rateDict.keys())]
        rate_change_time = sorted(self._rateDict.keys())  # sort the change_time increasingly
        # update rate once input period is larger than certain change_time
        for next_rate_change_time in rate_change_time:
            if period < next_rate_change_time:
                break
            rate = self._rateDict[next_rate_change_time]
        return rate
