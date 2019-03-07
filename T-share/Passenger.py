#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

class Passenger:
    def __init__(self, passenger_id):
        x_coord = random.randint(1,100)
        y_coord = random.randint(1,100)
        self.cur_location = [x_coord, y_coord]
        self.passenger_id = passenger_id

    def __str__(self):
        return 'The passenger id: %d, current location: [%d, %d]'%(self.passenger_id, self.cur_location[0], self.cur_location[1])

#############################
#           Test
#############################
# for i in range(10):
#     passenger = Passenger(i)
#     print(passenger)