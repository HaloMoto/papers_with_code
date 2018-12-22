#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' A Large-Service Dynamic Taxi Ridesharing Service '

__author__ = 'Xiangyuan Yang'

import time

class Query(Object):
    def __init__(self, pickup_point, delivery_point, pickup_early, pickup_late, delivery_early, delivery_late, submit_time):
        self.pickup_point = pickup_point
        self.delivery_point = delivery_point
        self.pickup_early = pickup_early
        self.pickup_late = pickup_late
        self.delivery_early = delivery_early
        self.delivery_late = delivery_late
        self.submit_time = submit_time

class Taxi(Object):
    def __init__(self, id, current_time, geographical_location, number_of_onboard_passengers, schedule, seat_capacity):
        self.id = id
        self.current_location = geographical_location
        self.current_time = current_time
        self.number_of_onboard_passengers = number_of_onboard_passengers
        self.schedule = schedule
        self.seat_capacity = seat_capacity

    def time_required(self, location_A, location_B): # 计算出租车当前位置到query的pickup point的时间
        pass

    def satisfaction(self, query):
        if self.number_of_onboard_passengers > self.seat_capacity:
            return False
        elif self.current_time + self.time_required(self.current_location, query.pickup_point) >  query.pickup_late:
            return False
        elif self.current_time + self.time_required():
            return False
        else:
            return True

    stream_of_queries = [Query(),Query()]