''''
Purpose: This module is to create house type classes
Author: Mengheng
Date: 10/24/2018
'''

from house_base import HouseBase


# PrimaryHome and VacationHome classes are derived from HouseBase class
# I override the annualDeprRate() method in these derived classes and
# provide the annual depreciate rate for each house types,
# so each house type classes are concrete classes
# a vacation home will depreciate slower than a primary home since it is often vacant
class PrimaryHome(HouseBase):
    def __init__(self, val):
        super(PrimaryHome, self).__init__(val)
        self._dep_rate = 0.4

    # override the annualDeprRate() method in HouseBase class to make the class concrete
    def annualDeprRate(self):
        return self._dep_rate


class VacationHome(HouseBase):
    def __init__(self, val):
        super(VacationHome, self).__init__(val)
        self._dep_rate = 0.1

    def annualDeprRate(self):
        return self._dep_rate
