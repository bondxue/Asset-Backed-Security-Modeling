'''
3.4.2
Purpose: This module is to create timer class.
update: 10/31/2018  add __enter__() and __exit__() to make Timer class work as a context manager.
                    add _timerName parameter in __init__()
                    add configureTimerDisplay() function
Author: Mengheng
Date: 10/31/2018
'''

import time


class Timer(object):

    # initialization function
    def __init__(self, timerName):
        self._start = 0  # record start time
        self._end = 0  # record end time
        self._is_started = False  # flag of start status
        self._timerName = timerName  # timer name
        self._format_type = 'second'  # format type
        self._last_time_record = -1  # initialize _last_time_record as -1 to avoid no _last_time_record case

    # function to record start time
    def start(self):
        # if the timer is already started, throw a running time error
        if self._is_started:
            raise RuntimeError('Timer is already started.')
        self._start = time.time()
        self._is_started = True  # execute only the first time to call start()

    # function to record end time and time taken
    def end(self):
        # if the Timer is not currently running, throw a running time error
        if not self._is_started:
            raise RuntimeError('Timer is not currently running.')
        self._end = time.time()  # end time record
        time_taken = self._end - self._start  # time taken record
        self.display_format(time_taken)
        self._last_time_record = time_taken  # record the current time_taken as last_time_record

    # function to configure the Timer to display either seconds, minutes or hours
    def display_format(self, seconds):  # default display format is seconds
        if self._format_type == 'hours':
            print '{}: {} hrs'.format(self._timerName, seconds / 3600.0)
        if self._format_type == 'minutes':
            print '{}: {} mins'.format(self._timerName, seconds / 60.0)
        if self._format_type == 'seconds':
            print '{}: {} s'.format(self._timerName, seconds)

    def configureTimerDisplay(self, format_type):
        self._format_type = format_type

    # function to retrieve the last timer result
    def record_last_timer(self):
        # if _last_time_record is still default -1, it means no last time record, throw error
        # otherwise, return last time record
        if self._last_time_record < 0:
            raise RuntimeError('No last time record.')
        # call display_format function to display the same time format as last time
        self.display_format(self._last_time_record)

    # enter context function
    def __enter__(self):
        self.start()
        self.configureTimerDisplay(format_type='seconds')  # default format_type is second
        return self  # must return self, which will assign to the 'as' variable in 'with...as..'

    # exit context function
    def __exit__(self, type, value, traceback):
        self.end()
