#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from Auxiliary import *
import datetime

class Query:
    def __init__(self, query_id):
        self.query_id = query_id
        x_coord_source = random.randint(1,20)
        y_coord_source = random.randint(1,20)
        x_coord_destination = random.randint(1,20)
        y_coord_destination = random.randint(1,20)
        self.source = [x_coord_source, y_coord_source]
        self.destination = [x_coord_destination, y_coord_destination]
        self.pickup_window = [0, random.randint(1,3)]
        self.delivery_window = [cal_distance(self.source, self.destination), cal_distance(self.source, self.destination)+random.randint(1,3)+self.pickup_window[1]]

    def __init__(self, query_id, current_time):
        self.query_id = query_id
        x_coord_source = random.randint(1,20)
        y_coord_source = random.randint(1,20)
        x_coord_destination = random.randint(1,20)
        y_coord_destination = random.randint(1,20)
        self.source = [x_coord_source, y_coord_source]
        self.destination = [x_coord_destination, y_coord_destination]
        self.pickup_window = [current_time, current_time+datetime.timedelta(seconds=random.randint(1,3))]
        self.delivery_window = [current_time + datetime.timedelta(seconds=cal_distance(self.source, self.destination)), datetime.timedelta(seconds=cal_distance(self.source, self.destination) + random.randint(1,3)) + self.pickup_window[1]]

    def __str__(self):
        return 'The query id: %d, the source: (%d, %d), the destination: (%d, %d)'%(self.query_id, self.source[0], self.source[1], self.destination[0], self.destination[1])

    # The method can judge whether the query is responded or not.
    def is_received(self, current_time):
        if self.pickup_window[1] < current_time:
            return False

########################################
#               Test1
########################################
# q = Query(1)
# print(q)

################
#    Test 2
################
# q = Query(1,datetime.datetime.now())
# print(q)
# print(q.pickup_window)
# print(q.delivery_window)