'''
Purpose: This module is to create Asset class
Author: Mengheng
Date: 10/24/2018
'''


# abstract Asset class
class Asset(object):
    # initialization function that save initial asset value
    def __init__(self, val):
        self._val = val

    # function to return yearly depreciation rate
    # trigger a non-implemented error
    # no one can directly instantiate an Asset object, make this abstract class
    def annualDeprRate(self):
        return 0.1
        # raise NotImplementedError()

    # function to return monthly depreciation rate
    def monthlyDepreRate(self):
        return self.annualDeprRate() / 12.0

    # function to return current value of asset
    def current_val(self, period):
        return self._val * (1 - self.monthlyDepreRate()) ** period
