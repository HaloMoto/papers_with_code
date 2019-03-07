#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
starttime = datetime.datetime(2014, 2, 1, 0, 0, 0) # Setting initial value to pool window start time.

endtime = datetime.datetime(2014, 2, 1, 0, 0, 1) #Setting initial value to pool window End time

untildatetime = datetime.datetime(2014, 2, 1, 0, 5, 0) # End date and time

windowsize = datetime.timedelta(0, 1) # Setting the window size