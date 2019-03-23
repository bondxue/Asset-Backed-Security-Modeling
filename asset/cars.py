''''
Purpose: This module is to create car types classes
Author: Mengheng
Date: 10/24/2018
'''

from car_base import Car


# multiple car types classes are derived from Car class
# I override the annualDeprRate() method in the car types classes and
# provide the annual depreciate rate for each car types,
# so each car type classes are concrete classes

class Civic(Car):
    def __init__(self, val):
        super(Civic, self).__init__(val)
        self._dep_rate = 0.3

    # override the annualDeprRate() method in Car class to make the class concrete
    def annualDeprRate(self):
        return self._dep_rate


class Lexus(Car):
    def __init__(self, val):
        super(Lexus, self).__init__(val)
        self._dep_rate = 0.2

    def annualDeprRate(self):
        return self._dep_rate


class Lamborghini(Car):
    def __init__(self, val):
        super(Lamborghini, self).__init__(val)
        self._dep_rate = 0.4

    def annualDeprRate(self):
        return self._dep_rate
