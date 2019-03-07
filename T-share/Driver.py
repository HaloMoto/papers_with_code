#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np
from Auxiliary import *

class Driver:

    capacity = 4
    speed = 1 #一个时间单位走一个距离单位

    def __init__(self, driver_id):
        x_coord = random.randint(1,20)
        y_coord = random.randint(1,20)
        self.cur_location = [x_coord, y_coord]
        self.driver_id = driver_id
        self.num_of_occupied_position = 0
        self.cur_schedule = []
        self.route = []
        self.assist_t = 0

    def __str__(self):
        return 'The driver id: %d, current location: (%d, %d), number of occupied position: %d'%(self.driver_id, self.cur_location[0], self.cur_location[1], self.num_of_occupied_position)

    def add_passenger(self, num_of_passenger):
        self.num_of_occupied_position = self.num_of_occupied_position + num_of_passenger
        return self.num_of_occupied_position

    def get_num_of_seats_remaining(self):
        return Driver.capacity - self.num_of_occupied_position

    def does_it_reach_the_first_point_in_the_schedule(self):
        if self.cur_schedule:
            if self.cur_location == self.cur_schedule[0][0]:
                if self.cur_schedule[0][2] == 1:
                    self.add_passenger(-1)
                del self.cur_schedule[0]

    # def does_it_reach_the_first_point_in_the_route(self):
    #     if self.cur_location == self.route[0]:
    #         del self.route[0]

    # After t seconds, can we reach the next point?
    def reach_the_next_point(self, t):
        if not self.route:
            return
        t = t+self.assist_t
        if t * self.speed > D[get_which_grid_the_location_belongs_to(self.cur_location)-1][int(self.route[0])-1] / 2:
            old_location = self.cur_location
            if int(self.route[0]) % 20 == 0:
                self.cur_location = [int(int(self.route[0])/20),20]
            else:
                self.cur_location = [int(int(self.route[0])/20)+1,int(self.route[0])%20]
            del self.route[0]
            if not self.route:
                self.assist_t = 0
            else:
                self.assist_t = -(D[get_which_grid_the_location_belongs_to(old_location)-1][get_which_grid_the_location_belongs_to(self.cur_location)-1] / 2  - self.speed * t) / self.speed
            self.does_it_reach_the_first_point_in_the_schedule()
        else:
            self.assist_t = t

D = np.loadtxt('dist.txt')
################################
#           Test 1
################################
# for i in range(10):
#     p = Driver(i)
#     print(p)

################################
#           Test 2
################################
# p = Driver(1)
# p.add_passenger(2)
# print(p)
# print(p.get_num_of_seats_remaining())
##############
#  Test 3
##############
# d = Driver(1)
# d.cur_schedule.append([d.cur_location,1])
# print(d.cur_schedule)
# d.does_it_reach_the_first_point_in_the_schedule()
# print(d.cur_schedule)
