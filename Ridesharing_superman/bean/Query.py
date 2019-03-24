#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import datetime
import numpy as np

class Query:
    def __init__(self, query_id, pickup_location, delivery_location, current_time):
        # 订单id
        self.query_id = query_id
        # 订单状态？
        self.condition = 0
        # 订单接载点位置
        self.pickup_location = pickup_location
        # 订单传送点位置
        self.delivery_location = delivery_location
        # 订单生成时间
        self.generation_time = current_time
        # 最晚接载时间
        self.latest_pickup_time = current_time + datetime.timedelta(seconds=120)
        # 最晚传送时间
        self.latest_delivery_time = self.latest_pickup_time + datetime.timedelta(seconds=T[self.pickup_location-1][self.delivery_location-1]) + datetime.timedelta(seconds=60)

    # print Query对象，打印
    def __str__(self):
        return 'The query id: %id, the pickup location: %d, the delivery location: %d'%(self.query_id, self.pickup_location, self.delivery_location)

    # 判断订单是否得到响应
    def is_received(self, current_time):
        if self.latest_pickup_time < current_time:
            return False

T = np.loadtxt("time.txt")

#############################
#       Test 1
#############################
