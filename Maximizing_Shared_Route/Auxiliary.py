# -*- coding: utf-8 -*-

from Driver import Driver
from Rider import Rider

def cal_shortest_route_distance(source, destination):
    return sum(map(lambda i,j: abs(i-j), source, destination))

def get_which_grid_the_location_belongs_to(location):
    return 20*(location[0]-1)+location[1]

def get_shared_route_percentage(driver, rider):
    dist_of_source1_to_source2 = cal_shortest_route_distance(driver.source, rider.source) # The distance of driver's source to rider's source
    dist_of_source2_to_destination2 = cal_shortest_route_distance(rider.source, rider.destination) # The distance of rider's source to rider's destination
    dist_of_destination2_to_destination1 = cal_shortest_route_distance(rider.destination, driver.destination) # The distance of rider's destination to driver's destination
    return dist_of_source2_to_destination2 / (dist_of_source1_to_source2 + dist_of_source2_to_destination2 + dist_of_destination2_to_destination1)

# If shared_route_percentage larger or equal than shared_requirement, return True, otherwise, return False.
def is_satisfied_with_shared_requirement(shared_requirement, shared_route_percentage):
    return shared_requirement <= shared_route_percentage

def find_PI_0(driver_set):
    PI_0 = 1
    for driver in driver_set:
        if PI_0 > driver.sharing_requirement:
            PI_0 = driver.sharing_requirement
    return PI_0

####################################
#            Test 1
####################################
# print(get_which_grid_the_location_belongs_to([20,19]))

####################################
#           Test 2
####################################
# driver = Driver()
# rider = Rider()
# shared_route_percentage = get_shared_route_percentage(driver, rider)
# print("Shared route percentage:",shared_route_percentage)
# print("Whether the shared proportion meets the requirement or not:",is_satisfied_with_shared_requirement(driver.sharing_requirement, shared_route_percentage))
