# -*- coding: utf-8 -*-

import random

class Driver:
    def __init__(self):
        x_coord_source = random.randint(1, 20)
        y_coord_source = random.randint(1, 20)
        x_coord_destination = random.randint(1, 20)
        y_coord_destination = random.randint(1, 20)
        self.source = [x_coord_source, y_coord_source]
        self.destination = [x_coord_destination, y_coord_destination]
        self.sharing_requirement = random.uniform(0.6, 0.9)

    def __str__(self):
        return 'The source location: (%d, %d), the destination location: (%d, %d), the sharing requirement: %f.'%(self.source[0],self.source[1],self.destination[0],self.destination[1],self.sharing_requirement)

#########################################
#                 Test 1
#########################################
# driver = Driver()
# print(driver)

#########################################
#                 Test 2
#########################################
# for i in range(10):
#     driver = Driver()
#     print(driver)