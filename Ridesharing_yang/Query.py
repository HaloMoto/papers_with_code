#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from Auxiliary import *
import datetime
import numpy as np

class Query:
    def __init__(self, query_id, pickup_location, current_time):
        self.query_id = query_id
        self.pickup_location = pickup_location
        self.delivery_location = random.randint(246, 420) # Anchor numbers for each partition are 246 to 420
        self.generation_time = current_time
        self.latest_pickup_time = current_time + datetime.timedelta(seconds=120)
        self.latest_delivery_time = self.latest_pickup_time + datetime.timedelta(seconds=T[self.pickup_location-1][self.delivery_location-1]) + datetime.timedelta(seconds=120)

    def __str__(self):
        return 'The query id: %d, the pickup location: %d, the delivery location: %d'%(self.query_id, self.pickup_location, self.delivery_location)

    # The method can judge whether the query is responded or not
    def is_received(self, current_time):
        if self.latest_pickup_time < current_time:
            return False

T = np.loadtxt("time.txt")

########################
#       Test 1
########################
print(Query(1,299,datetime.datetime.now()))