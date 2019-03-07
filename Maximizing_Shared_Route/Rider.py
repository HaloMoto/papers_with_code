# -*- coding: utf-8 -*-

import random

class Rider:
    def __init__(self):
        x_coord_source = random.randint(1,20)
        y_coord_source = random.randint(1,20)
        x_coord_destination = random.randint(1,20)
        y_coord_destination = random.randint(1,20)
        self.source = [x_coord_source, y_coord_source]
        self.destination = [x_coord_destination, y_coord_destination]

    def __str__(self):
        return 'The source location: (%d, %d), the destination location: (%d, %d)'%(self.source[0],self.source[1],self.destination[0],self.destination[1])

#######################################
#                Test 1
#######################################
# rider = Rider()
# print(rider)