'''
Purpose: This module contains classes related to auto loan.
update: 10/31/2018   __init__ raise exception instead of print error message
        11/22/2018   replace term with start_date, end_date
        11/25/2018   change back to term
Author: Mengheng
Date: 10/31/2018
'''

from loans import FixedRateLoan
from asset.car_base import Car
import logging


# fixed rate autoloan class derived from FixedRateLoan
class AutoLoan(FixedRateLoan):
    # save car parameter as a Car object,
    # if not, print an error message and leave the function
    def __init__(self, term, rate, face, car):
        if not isinstance(car, Car):
            logging.error('input {} is not Car object.'.format(car))
            raise TypeError('Car parameter should be Car object.')
        super(AutoLoan, self).__init__(term, rate, face, car)
