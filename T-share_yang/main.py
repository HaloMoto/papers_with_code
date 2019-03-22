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
# 订单被接收时间减去订单生成时间
total_time = 0
total_distance = 0
total_distance_traveled = 0
number_of_order_variance = 0

for i in range(int(num_of_drivers)):
    driver_list.append(Driver(i, 200))

query_id = 1

while endtime <= Timeframe.untildatetime:
    # Generate orders
    for i in range(int(num_of_querys)):
        temp = random.randint(1,309)
        # print(temp)
        for j in range(len(hot_index)-1):
            if temp > hot_index[j] and temp <= hot_index[j+1]:
                partitions[j].statistic_of_order += 1
                query_list.append(Query(query_id, j-1+245, starttime))
                query_id += 1
                break
    # search module
    for query in query_list:
        t1 = datetime.datetime.now()
        satisfied_driver_list = dual_side_search(driver_list, query, starttime)
        t2 = datetime.datetime.now()
        # print("search:",(t2-t1).microseconds)
        # print(len(satisfied_driver_list))
        # for driver in satisfied_driver_list:
        #     print(driver.driver_id)
        t3 = datetime.datetime.now()
        for j in range(len(satisfied_driver_list)):
            # if not satisfied_driver_list[j].cur_schedule:
            #     if insertion_feasibility_check(query_list[i], satisfied_driver_list[j], 1, 1, 0):
            #         num_of_satisfied_query = num_of_satisfied_query + 1
            #         break
            # If schedule is empty, insert it directly.
            if not satisfied_driver_list[j].cur_schedule:
                satisfied_driver_list[j].number_of_order += 1
                number_of_order_served += 1
                total_time += (starttime - query.generation_time).seconds
                total_distance += D[query.pickup_location - 1][query.delivery_location - 1]
                # 如果一开始route非空
                if satisfied_driver_list[j].route:
                    satisfied_driver_list[j].cur_schedule.append([query.pickup_location, query.latest_pickup_time, 0])
                    first_location_origin_route = satisfied_driver_list[j].route[0]
                    satisfied_driver_list[j].route = []
                    satisfied_driver_list[j].route.extend(
                        (str(satisfied_driver_list[j].cur_location) + obtainPath(
                            satisfied_driver_list[j].cur_location - 1,
                            query.pickup_location - 1) + str(
                            query.pickup_location)).split())
                    satisfied_driver_list[j].cur_schedule.append([query.delivery_location, query.latest_delivery_time, 1])
                    satisfied_driver_list[j].route.extend(
                        (str(query.pickup_location) + obtainPath(
                            query.pickup_location - 1,
                            query.delivery_location - 1) + str(
                            query.delivery_location)).split())
                    del satisfied_driver_list[j].route[0]
                    if satisfied_driver_list[j].route[0] == first_location_origin_route:
                        satisfied_driver_list[j].assist_t = satisfied_driver_list[j].assist_t
                    else:
                        satisfied_driver_list[j].assist_t = -abs(satisfied_driver_list[j].assist_t)
                # 如果一开始route为空
                else:
                    satisfied_driver_list[j].cur_schedule.append([query.pickup_location, query.latest_pickup_time, 0])
                    satisfied_driver_list[j].route = []
                    satisfied_driver_list[j].route.extend(
                        (str(satisfied_driver_list[j].cur_location) + obtainPath(
                            satisfied_driver_list[j].cur_location - 1,
                            query.pickup_location - 1) + str(
                            query.pickup_location)).split())
                    satisfied_driver_list[j].cur_schedule.append(
                        [query.delivery_location, query.latest_delivery_time, 1])
                    satisfied_driver_list[j].route.extend(
                        (str(query.pickup_location) + obtainPath(
                            query.pickup_location - 1,
                            query.delivery_location - 1) + str(
                            query.delivery_location)).split())
                    del satisfied_driver_list[j].route[0]
                # 增加一个顾客
                satisfied_driver_list[j].add_passenger(1)
                # 将订单状态设置为已服务状态
                query.condition = 1
                break
            # 寻找订单接载点和传送点插入的位置
            for m in range(1, int(len(satisfied_driver_list[j].cur_schedule))+1):
                for n in range(m,int(len(satisfied_driver_list[j].cur_schedule))+2):
                    if insertion_feasibility_check(query, satisfied_driver_list[j], m, n, starttime):
                        # print(satisfied_driver_list[j].num_of_occupied_position)
                        satisfied_driver_list[j].number_of_order += 1
                        number_of_order_served += 1

                        # print('hello')
                        query.condition = 1
                        break
                else:
                    continue
                break
            else:
                continue
            break
        t4 = datetime.datetime.now()
        # print("infeasible:",(t4-t3).microseconds)

    # Refresh the route of empty drivers
    recommendation(driver_list)

    # Refresh the location of drivers
    for driver in driver_list:
        if driver.num_of_occupied_position > 0 and driver.num_of_occupied_position*2 != len(driver.cur_schedule):
            driver.total_time_traveled += Timeframe.windowsize.seconds
        driver.reach_the_next_point((endtime-starttime).seconds)
        if driver.driver_id == 0:
            print(driver.cur_location)
            print(driver.cur_schedule)
        # print(driver.cur_schedule)

    # Delete satisfied queries
    query_list = [query for query in query_list if query.condition == 0]

    # Delete expired queries
    query_list = [query for query in query_list if endtime > query.latest_pickup_time]

    # # Update hot index
    # if (starttime - Timeframe.starttime).seconds % 60 == 0:
    #     for partition in partitions:
    #         partition.hot_index = partition.statistic_of_order
    #         partition.statistic_of_order = 0

    starttime = endtime
    endtime = endtime + Timeframe.windowsize

# 算法结束时，有的车还没有跑完route中的所有点，在这里接着跑完：
while True:
    sign = True
    for driver in driver_list:
        if driver.num_of_occupied_position != 0:
            sign = False
        if driver.num_of_occupied_position > 0 and driver.num_of_occupied_position*2 != len(driver.cur_schedule):
            driver.total_time_traveled += Timeframe.windowsize.seconds
        driver.reach_the_next_point(Timeframe.windowsize.seconds)
    if sign:
        break

total_order = query_id
# Calculate total distance drivers traveled
for driver in driver_list:
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
print("Passenger service rate:",number_of_order_served / total_order)
print("Total distance saving:",total_distance - total_distance_traveled)
print("Variance of Driver Reception Number:",number_of_order_variance)