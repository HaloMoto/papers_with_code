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
# Use hot_index to produce order and add 1 for each partition's hot_index
hot_index = []
hot_index.append(0)
for partition in partitions:
    partition.hot_index += 1
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
    driver_list.append(Driver(i, 200))

query_id = 1

while endtime <= Timeframe.untildatetime:
    # #the location of each driver:
    # for driver in driver_list:
    #     print("The current location of driver:",driver.cur_location)
    # Generate orders
    for i in range(int(num_of_querys)):
        temp = random.randint(1,484)
        # print(temp)
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
        # if len(empty_driver_list) == 0:
        #     print("0")
        if empty_driver_list:
            sign0 = False
            for driver in empty_driver_list:
                if starttime + datetime.timedelta(seconds=T[driver.cur_location-1][query.pickup_location]) < query.latest_pickup_time:
                    driver.cur_schedule.append([query.pickup_location, query.latest_pickup_time, 0])
                    #如果一开始route非空
                    if driver.route:
                        first_location_origin_route = driver.route[0]
                        driver.route = []
                        driver.route.extend(
                            (str(driver.cur_location) + obtainPath(
                                driver.cur_location-1,query.pickup_location-1) + str(
                                query.pickup_location)).split())
                        driver.cur_schedule.append([query.delivery_location, query.latest_delivery_time, 1])
                        driver.route.extend(
                            (obtainPath(
                                query.pickup_location - 1, query.delivery_location - 1) + str(
                                query.delivery_location)).split())
                        del driver.route[0]
                        if driver.route[0] == first_location_origin_route:
                            driver.assist_t = driver.assist_t
                        else:
                            driver.assist_t = -abs(driver.assist_t)
                    #一开始为空
                    else:
                        driver.route = []
                        driver.route.extend(
                            (str(driver.cur_location) + obtainPath(
                                driver.cur_location - 1, query.pickup_location - 1) + str(
                                query.pickup_location)).split())
                        driver.cur_schedule.append([query.delivery_location, query.latest_delivery_time, 1])
                        driver.route.extend(
                            (obtainPath(
                                query.pickup_location - 1, query.delivery_location - 1) + str(
                                query.delivery_location)).split())
                        del driver.route[0]
                    driver.add_passenger(1)
                    # print("123",driver.cur_schedule)
                    # print("234",driver.num_of_occupied_position)
                    driver.number_of_order += 1
                    query.condition = 1
                    number_of_order_served += 1
                    total_time += (starttime - query.generation_time).seconds
                    total_distance += D[query.pickup_location-1][query.delivery_location-1]
                    sign0 = True
                    break
            if sign0:
                continue
        # Search one passenger driver
        one_passenger_driver_list = one_passenger_driver_search(driver_list, query, starttime)
        if one_passenger_driver_list:
            sign1 = False
            for j in range(len(one_passenger_driver_list)):
                for m in range(1, int(len(one_passenger_driver_list[j].cur_schedule))+1):
                    for n in range(m, int(len(one_passenger_driver_list[j].cur_schedule))+2):
                        if insertion_feasibility_check(query, one_passenger_driver_list[j], m, n, starttime):
                            # print("2")
                            query.condition = 1
                            number_of_order_served += 1
                            one_passenger_driver_list[j].number_of_order += 1
                            total_time += (starttime - query.generation_time).seconds
                            total_distance += D[query.pickup_location-1][query.delivery_location-1]
                            sign1 = True
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            if sign1:
                continue
        # Search two passenger driver
        two_passenger_driver_list = two_passenger_driver_search(driver_list, query, starttime)
        if two_passenger_driver_list:
            sign2 = False
            for j in range(len(two_passenger_driver_list)):
                for m in range(1, int(len(two_passenger_driver_list[j].cur_schedule)) + 1):
                    for n in range(m, int(len(two_passenger_driver_list[j].cur_schedule)) + 2):
                        # print("3",n)
                        if insertion_feasibility_check(query, two_passenger_driver_list[j], m, n, starttime):
                            # print("3")
                            query.condition = 1
                            number_of_order_served += 1
                            two_passenger_driver_list[j].number_of_order += 1
                            total_time += (starttime - query.generation_time).seconds
                            total_distance += D[query.pickup_location-1][query.delivery_location-1]
                            sign2 = True
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            if sign2:
                continue
        # Search three passenger driver
        three_passenger_driver_list = three_passenger_driver_search(driver_list, query, starttime)
        if three_passenger_driver_list:
            sign3 = False
            for j in range(len(three_passenger_driver_list)):
                for m in range(1, int(len(three_passenger_driver_list[j].cur_schedule)) + 1):
                    for n in range(m, int(len(three_passenger_driver_list[j].cur_schedule)) + 2):
                        # print("4",n)
                        if insertion_feasibility_check(query, three_passenger_driver_list[j], m, n, starttime):
                            # print("4")
                            query.condition = 1
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
            if sign3:
                continue

    # # Refresh the route of empty drivers
    # recommendation(driver_list)
    recommendation1(driver_list)

    # Refresh the location of drivers
    for driver in driver_list:
        if driver.num_of_occupied_position > 0 and driver.num_of_occupied_position*2 != len(driver.cur_schedule):
            driver.total_time_traveled += (endtime-starttime).seconds
        driver.reach_the_next_point((endtime-starttime).seconds)
        if driver.driver_id == 0:
            print("--------------------------------------------")
            print(starttime)
            print(driver.cur_location)
            print(driver.cur_schedule)
            print(driver.route)
            print(driver.assist_t)
            print(driver.num_of_occupied_position)
            print(driver.total_time_traveled)
        # if driver.num_of_occupied_position > 1:
        #     print(driver.driver_id)

    # Delete satisfied queries
    print("查询总数：",len(query_list))
    query_list = [query for query in query_list if query.condition == 0]
    print("删除被服务的查询后的剩下查询数：",len(query_list))

    # Delete expired queries
    query_list = [query for query in query_list if endtime > query.latest_pickup_time]
    print("删除过期查询后：",len(query_list))

    # Update hot index
    if (starttime - Timeframe.starttime).seconds % 60 == 0:
        for partition in partitions:
            partition.hot_index = partition.statistic_of_order
            partition.statistic_of_order = 0

    starttime = endtime
    endtime = endtime + Timeframe.windowsize
    # print(endtime)

# 算法结束时，有的车还没有跑完route中的所有点，在这里接着跑完：
while True:
    sign = True
    for driver in driver_list:
        # print(driver.num_of_occupied_position)
        if driver.num_of_occupied_position != 0:
            sign = False
        if driver.num_of_occupied_position > 0 and driver.num_of_occupied_position*2 != len(driver.cur_schedule):
            driver.total_time_traveled += Timeframe.windowsize.seconds
        driver.reach_the_next_point(Timeframe.windowsize.seconds)
        # print(driver.cur_schedule)
    if sign:
        break

# for driver in driver_list:
#     print("route:",driver.route)

total_order = query_id
# Calculate total distance drivers traveled
for driver in driver_list:
    # print(driver.total_time_traveled)
    total_distance_traveled += driver.total_time_traveled * driver.speed

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
print("Passenger service rate:",number_of_order_served / (total_order-len(query_list)))
print("Total distance saving:",total_distance - total_distance_traveled)
print("Variance of Driver Reception Number:",number_of_order_variance)