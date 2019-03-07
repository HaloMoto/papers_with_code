#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Timeframe
from Algorithm import *
from Driver import Driver
from Query import Query
from partition import Partition
import pickle
import random
from Auxiliary import obtainPath
import numpy as np

starttime = Timeframe.starttime
endtime = Timeframe.endtime
# Load partitions
with open('partitions.txt','rb') as f:
    partitions = pickle.load(f)
# Load dist.txt
D = np.loadtxt('dist.txt')
# Use hot_index to produce order
hot_index = []
hot_index.append(0)
for partition in partitions:
    hot_index.append(hot_index[-1]+partition.hot_index)

num_of_drivers = input('Please enter the number of drivers:')
num_of_querys = input('How many queries per second on average:')

driver_list = []
query_list = []
total_order = 0
number_of_order_served = 0
total_time = 0
total_distance = 0
total_distance_traveled = 0
number_of_order_variance = 0

for i in range(int(num_of_drivers)):
    driver_list.append(Driver(i, 1000))

query_id = 1

while endtime <= Timeframe.untildatetime:
    # Generate orders
    for i in range(int(num_of_querys)):
        temp = random.randint(1,309)
        print(temp)
        for j in range(len(hot_index)-1):
            if temp > hot_index[j] and temp <= hot_index[j+1]:
                partitions[j].statistic_of_order += 1
                query_list.append(Query(query_id, j-1+245, starttime))
                query_id += 1
                break

    # Search for each order
    for query in query_list:
        # Search empty driver
        empty_driver_list = empty_driver_search(driver_list, query, starttime)
        if empty_driver_list:
            empty_driver_list[0].cur_schedule.append([query.pickup_location, query.latest_pickup_time, 0])
            empty_driver_list[0].route = []
            empty_driver_list[0].route.extend(
                (str(empty_driver_list[0].cur_location) + obtainPath(
                    empty_driver_list[0].cur_location-1,query.pickup_location-1) + str(
                    query.pickup_location)).split())
            empty_driver_list[0].cur_schedule.append([query.delivery_location, query.latest_delivery_time, 1])
            empty_driver_list[0].route.extend(
                (str(query.pickup_location) + obtainPath(
                    query.pickup_location - 1, query.delivery_location - 1) + str(
                    query.delivery_location)).split())
            empty_driver_list[0].add_passenger(1)
            empty_driver_list[0].number_of_order += 1
            query_list.remove(query)
            number_of_order_served += 1
            total_time += (starttime - query.generation_time).seconds
            total_distance += D[query.pickup_location-1][query.delivery_location-1]
            continue
        # Search one passenger driver
        one_passenger_driver_list = one_passenger_driver_search(driver_list, query, starttime)
        if one_passenger_driver_list:
            for j in range(len(one_passenger_driver_list)):
                for m in range(1, int(len(one_passenger_driver_list[j].cur_schedule))+1):
                    for n in range(m, int(len(one_passenger_driver_list[j].cur_schedule))+2):
                        if insertion_feasibility_check(query, one_passenger_driver_list[j], m, n, starttime):
                            query_list.remove(query)
                            number_of_order_served += 1
                            one_passenger_driver_list[j].number_of_order += 1
                            total_time += (starttime - query.generation_time).seconds
                            total_distance += D[query.pickup_location-1][query.delivery_location-1]
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            continue
        # Search two passenger driver
        two_passenger_driver_list = two_passenger_driver_search(driver_list, query, starttime)
        if two_passenger_driver_list:
            for j in range(len(two_passenger_driver_list)):
                for m in range(1, int(len(two_passenger_driver_list[j].cur_schedule)) + 1):
                    for n in range(m, int(len(two_passenger_driver_list[j].cur_schedule)) + 2):
                        if insertion_feasibility_check(query, two_passenger_driver_list[j], m, n, starttime):
                            query_list.remove(query)
                            number_of_order_served += 1
                            two_passenger_driver_list[j].number_of_order += 1
                            total_time += (starttime - query.generation_time).seconds
                            total_distance += D[query.pickup_location-1][query.delivery_location-1]
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            continue
        # Search three passenger driver
        three_passenger_driver_list = three_passenger_driver_search(driver_list, query, starttime)
        if three_passenger_driver_list:
            for j in range(len(three_passenger_driver_list)):
                for m in range(1, int(len(three_passenger_driver_list[j].cur_schedule)) + 1):
                    for n in range(m, int(len(three_passenger_driver_list[j].cur_schedule)) + 2):
                        if insertion_feasibility_check(query, three_passenger_driver_list[j], m, n, starttime):
                            query_list.remove(query)
                            number_of_order_served += 1
                            three_passenger_driver_list[j].number_of_order += 1
                            total_time += (starttime - query.generation_time).seconds
                            total_distance += D[query.pickup_location-1][query.delivery_location-1]
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            continue

    # Refresh the route of empty drivers
    recommendation(driver_list)

    # Refresh the location of drivers
    for driver in driver_list:
        driver.reach_the_next_point((endtime-starttime).seconds)

    # Delete expired queries
    for query in query_list:
        if endtime > query.latest_pickup_time:
            query_list.remove(query)

    # Update hot index
    if (starttime - Timeframe.starttime).seconds % 60 == 0:
        for partition in partitions:
            partition.hot_index = partition.statistic_of_order
            partition.statistic_of_order = 0

    starttime = endtime
    endtime = endtime + Timeframe.windowsize

total_order = query_id
# Calculate total distance drivers traveled
for driver in driver_list:
    total_distance_traveled += driver.total_distance_traveled

# Calculate the variance of the number of passengers received by each driver
number_of_orders = []
for driver in driver_list:
    number_of_orders.append(driver.number_of_order)
number_of_order_variance = np.var(number_of_orders)
print(number_of_orders)
print(np.sum(number_of_orders))
print(np.mean(number_of_orders))

print(total_order)
print(total_distance)
print(total_distance_traveled)
print("Average waiting time:",total_time / number_of_order_served)
print("Passenger service rate:",number_of_order_served / total_order)
print("Total distance saving:",total_distance - total_distance_traveled)
print("Variance of Driver Reception Number:",number_of_order_variance)