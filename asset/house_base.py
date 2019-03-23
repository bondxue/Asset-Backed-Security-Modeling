'''
Purpose: This module is to create Housebase abstract class
Author: Mengheng
Date: 10/24/2018
'''

from asset import Asset


# Housebase class is derived from Asset class
# notice that I didn't override the annualDeprRate() function in Asset here
# so Housebase class is still a abstract class
class HouseBase(Asset):
    def __init__(self, val):
        super(HouseBase, self).__init__(val)
