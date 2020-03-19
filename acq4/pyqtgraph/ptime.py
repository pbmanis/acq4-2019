# -*- coding: utf-8 -*-
"""
ptime.py -  Precision time function made os-independent (should have been taken care of by python)
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more infomation.
"""


import sys
#import time as systime
import timeit  # Python 3.8 deprecates time
START_TIME = None
time = None

def winTime():
    """Return the current time in seconds with high precision (windows version, use Manager.time() to stay platform independent)."""
#    return systime.clock() + START_TIME
    #return systime.time()
    return timeit.default_timer()

def unixTime():
    """Return the current time in seconds with high precision (unix version, use Manager.time() to stay platform independent)."""
    #return systime.time()
    return timeit.default_timer()

if sys.platform.startswith('win'):
    # cstart = systime.clock()  ### Required to start the clock in windows
    # START_TIME = systime.time() - cstart
    cstart =  timeit.default_timer()
    START_TIME = timeit.default_timer() - cstart

    time = winTime
else:
    time = unixTime

