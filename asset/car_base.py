'''
Purpose: This module is to create abstract Car class
Author: Mengheng
Date: 10/24/2018
'''

from asset import Asset


# Car class is derived from Asset class
# notice that I didn't override the annualDeprRate() function in Asset here
# so Car class is still a abstract class
class Car(Asset):
    def __init__(self, val):
        super(Car, self).__init__(val)
        self._dep_rate = 0.2
