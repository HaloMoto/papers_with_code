# -*- coding: utf-8 -*-

from Driver import Driver
from Rider import Rider
from Auxiliary import find_PI_0
from Algorithm import exact_join

num_of_drivers = input('Please enter the number of drivers:')
num_of_riders = input('Please enter the number of riders:')

driver_set = set()
rider_set = set()

for i in range(int(num_of_drivers)):
    driver_set.add(Driver())

for i in range(int(num_of_riders)):
    rider_set.add(Rider())

PI_0 = find_PI_0(driver_set)

matching = exact_join(rider_set, driver_set, PI_0)

print(matching)
print(len(matching))

##############################
#            Test 1
##############################
# for driver in driver_set:
#     print(driver)
#
# for rider in rider_set:
#     print(rider)
#############################
#            Test 2
# #############################
# print(PI_0)