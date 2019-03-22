#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np
from Auxiliary import *

class Driver:

    capacity = 4
    speed = 25 # The speed is 11 meters per second

    def __init__(self, driver_id, area_finding):
        self.cur_location = random.randint(1,420)
        self.driver_id = driver_id
        self.num_of_occupied_position = 0
        self.cur_schedule = []
        self.route = []
        self.assist_t = 0
        self.area_finding = area_finding
        self.number_of_order = 0
        self.total_time_traveled = 0
        self.total_distance_traveled = 0

    def __str__(self):
        return 'The driver id: %d, current location: (%d, %d), number of occupied position: %d.'%(self.driver_id, self.cur_location[0], self.cur_location[1], self.num_of_occupied_position)

    def add_passenger(self, num_of_passenger):
        self.num_of_occupied_position = self.num_of_occupied_position + num_of_passenger
        return self.num_of_occupied_position

    def get_num_of_seats_remaining(self):
        return Driver.capacity - self.num_of_occupied_position

    def does_it_reach_the_first_point_in_the_schedule(self):
        if self.cur_schedule:
            while True:
                if self.cur_schedule and self.cur_location == self.cur_schedule[0][0]:
                    if self.cur_schedule[0][2] == 1:
                        self.add_passenger(-1)
                        # print("helo")
                    del self.cur_schedule[0]
                else:
                    break

    # After t seconds, can we reach the next point?
    def reach_the_next_point(self, t):
        if not self.route:
            return
        while True:
            t = t + self.assist_t
            if not self.route:
                break
            if t * self.speed > D[self.cur_location-1][int(self.route[0])-1] / 2:
                old_location = self.cur_location
                self.cur_location = int(self.route[0])
                # Calculate the distance of a car when there are passengers on it
                # if self.num_of_occupied_position > 0 and self.num_of_occupied_position*2 != len(self.cur_schedule):
                #     self.total_distance_traveled += D[old_location-1][self.cur_location-1]
                del self.route[0]

                # self.assist_t = -(D[old_location-1][self.cur_location-1] / 2 - self.speed * t) / self.speed
                self.assist_t = (self.speed * t - D[old_location-1][self.cur_location-1]) / self.speed
                self.does_it_reach_the_first_point_in_the_schedule()
                t = 0
            else:
                self.assist_t = t
                break

D = np.loadtxt('dist.txt')

