#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Driver import Driver
from Query import Query
from functools import cmp_to_key
import numpy as np
from Auxiliary import obtainPath
import datetime
import pickle
import random

# Load partitions
with open('partitions.txt','rb') as f:
    partitions = pickle.load(f)

# Load nodes_belong_to_which_partition.txt
with open('nodes_belong_to_which_partition.txt','rb') as f:
    nodes_belong_to_which_partition = pickle.load(f)

def dual_side_search(driver_list, query, t_cur):
    g_o = query.pickup_location
    S_o = list(filter(lambda driver: t_cur + datetime.timedelta(
        seconds=T[g_o - 1][driver.cur_location - 1]) <= query.latest_pickup_time and driver.num_of_occupied_position < 4, driver_list))
    S_o.sort(key=cmp_to_key(
        lambda driver1, driver2: D[g_o - 1][driver1.cur_location - 1] - D[g_o - 1][driver2.cur_location - 1]))
    # print(S_o)
    g_d = query.delivery_location
    S_d = list(filter(lambda driver: t_cur + datetime.timedelta(seconds=T[g_d - 1][driver.cur_location - 1]) <= query.latest_delivery_time and driver.num_of_occupied_position < 4, driver_list))
    S_d.sort(key=cmp_to_key(lambda driver1, driver2: D[g_d - 1][driver1.cur_location - 1] - D[g_d - 1][driver2.cur_location - 1]))
    # print(S_d)
    S_intersection = list(set(S_o).intersection(set(S_d)))
    # print(len(S_intersection))
    # print("1")
    # l_o = []
    # # for g_i in Gt[get_which_grid_the_location_belongs_to(g_o)]:
    # #     if g_i == 400:
    # #         print(int(g_i))
    # for g_i in Gt[nodes_belong_to_which_partition[g_o] - 1]:
    #     if t_cur + datetime.timedelta(seconds=T[g_o - 1][int(g_i) + 245 - 1]) <= \
    #             query.latest_pickup_time:
    #         l_o.append(g_i)
    #     else:
    #         break
    #
    # # print("2")
    # l_d = []
    # for g_j in Gt[nodes_belong_to_which_partition[g_d] - 1]:
    #     if t_cur + datetime.timedelta(seconds=T[g_d - 1][int(g_j) + 245 - 1]) <= \
    #             query.latest_delivery_time:
    #         l_d.append(g_j)
    #     else:
    #         break;
    #
    # stop_o = False
    # stop_d = False
    # # print("3")
    # while not S_intersection and (stop_o == False or stop_d == False):
    #     # print("yes")
    #     if l_o:
    #         g_i = l_o.pop(0)
    #         S_o = list(set(S_o).union(set(list(filter(lambda driver: T[int(g_i) + 245 - 1, driver.cur_location - 1] <= (query.latest_pickup_time - t_cur).seconds, driver_list)))))
    #         S_o.sort(key=cmp_to_key(lambda driver1, driver2: D[int(g_i) + 245 - 1, driver1.cur_location - 1] - D[int(g_i) + 245 - 1, driver2.cur_location - 1]))
    #     else:
    #         stop_o = True
    #     if l_d:
    #         g_j = l_d.pop(0)
    #         S_d = list(set(S_d).union(set(list(filter(
    #             lambda driver: T[int(g_j) + 245 - 1, driver.cur_location - 1] <= (query.latest_delivery_time - t_cur).seconds, driver_list)))))
    #         S_d.sort(key=cmp_to_key(lambda driver1, driver2: D[int(g_j) + 245 - 1, driver1.cur_location - 1] - D[int(g_j) + 245 - 1, driver2.cur_location - 1]))
    #     else:
    #         stop_d = True
    #     S_intersection = list(set(S_o).intersection(set(S_d)))
    #     # print(S_intersection)

    return S_intersection

def insertion_feasibility_check(query, driver, m, n, t_cur):
    # Calculate the time from driver.cur_location to query.pickup_location
    t_i = 0
    if m == 1:
        t_i = t_i + T[driver.cur_location-1][query.pickup_location-1]
    else:
        t_i = t_i + T[driver.cur_location-1][driver.cur_schedule[0][0]-1]
        for i in range(m-2):
            t_i = t_i + T[driver.cur_schedule[i][0]-1][driver.cur_schedule[i+1][0]-1]
        t_i = t_i + T[driver.cur_schedule[m-2][0]-1][query.pickup_location-1]

    if t_cur + datetime.timedelta(seconds=t_i) > query.latest_pickup_time:
        return False

    # Check the time delay incurred by the insertion of query.pickup_location causes the slack time of any point after position i in schedule V.s smaller than 0
    t_i = t_i + T[query.pickup_location-1][driver.cur_schedule[m-1][0]-1]
    if t_cur + datetime.timedelta(seconds=t_i) > driver.cur_schedule[m-1][1]:
        return False
    for i in range(m,len(driver.cur_schedule)):
        t_i = t_i + T[driver.cur_schedule[i-1][0]-1][driver.cur_schedule[i][0]-1]
        if t_cur + datetime.timedelta(seconds=t_i) > driver.cur_schedule[i][1]:
            return False
    driver.cur_schedule.insert(m-1,[query.pickup_location, query.latest_pickup_time, 0]) # Insert query.pickup_location into driver.cur_schedule at position m

    # Calculate the time from driver.cur_location to query.destination
    t_j = 0
    t_j = t_j + T[driver.cur_location-1][driver.cur_schedule[0][0]-1]
    for j in range(n + 1 - 2):
        t_j = t_j + T[driver.cur_schedule[j][0]-1][driver.cur_schedule[j+1][0]-1]
    t_j = t_j + T[driver.cur_schedule[n + 1 - 2][0]-1][query.delivery_location-1]

    if t_cur + datetime.timedelta(seconds=t_j) > query.latest_delivery_time:
        del driver.cur_schedule[m-1]
        return False
    elif n == len(driver.cur_schedule):
        driver.cur_schedule.insert(n + 1 - 1, [query.delivery_location, query.latest_delivery_time,1])  # Insert query.delivery_location into driver.cur_schedule as position n

        driver.add_passenger(1)
        #原来路径的第一个点
        first_location_origin_route = driver.route[0]
        # Recalculate route after schedule change
        driver.route = []
        driver.route.extend(
            (str(driver.cur_location) + obtainPath(
                driver.cur_location - 1, driver.cur_schedule[0][0] - 1) + str(
                driver.cur_schedule[0][0])).split())
        for i in range(len(driver.cur_schedule) - 1):
            driver.route.extend(
                (str(driver.cur_schedule[i][0]) + obtainPath(
                    driver.cur_schedule[i][0] - 1, driver.cur_schedule[i + 1][0] - 1) + str(
                    driver.cur_schedule[i + 1][0])).split())
        del driver.route[0]
        # 如果调整之后的路径第一个点和原始路径第一个点相同
        if driver.route[0] == first_location_origin_route:
            driver.assist_t = driver.assist_t
        else:
            driver.assist_t = -abs(driver.assist_t)

        return True

    #Check the time delay incurred by the insertion of query.source causes the slack time of any point after position i in schedule V.s smaller than 0
    t_j = t_j + T[query.delivery_location-1][driver.cur_schedule[n+1-1][0]-1]
    if t_cur + datetime.timedelta(seconds=t_j) > driver.cur_schedule[n+1-1][1]:
        del driver.cur_schedule[m-1]
        return False
    for j in range(n+1, len(driver.cur_schedule)):
        t_j = t_j + T[driver.cur_schedule[j-1][0]-1][driver.cur_schedule[j][0]-1]
        if t_cur + datetime.timedelta(seconds=t_j) > driver.cur_schedule[j][1]:
            del driver.cur_schedule[m-1]
            return False
    driver.cur_schedule.insert(n + 1 - 1, [query.delivery_location, query.latest_delivery_time, 1]) # Insert query.delivery_location into driver.cur_schedule as position n

    driver.add_passenger(1)

    first_location_origin_route = driver.route[0]
    # Recalculate route after schedule change
    driver.route = []
    driver.route.extend(
        (str(driver.cur_location) + obtainPath(
            driver.cur_location - 1, driver.cur_schedule[0][0] - 1) + str(
            driver.cur_schedule[0][0])).split())
    for i in range(len(driver.cur_schedule)-1):
        driver.route.extend(
            (str(driver.cur_schedule[i][0]) + obtainPath(
                driver.cur_schedule[i][0] - 1, driver.cur_schedule[i+1][0] - 1) + str(
                driver.cur_schedule[i+1][0])).split())
    del driver.route[0]
    if driver.route[0] == first_location_origin_route:
        driver.assist_t = driver.assist_t
    else:
        driver.assist_t = -abs(driver.assist_t)

    return True


def recommendation(driver_list):
    for driver in driver_list:
        if driver.num_of_occupied_position == 0 and not driver.route:
            # part_id_of_driver = nodes_belong_to_which_partition[driver.cur_location]
            # partition_in_range = []
            # for i in Gd[part_id_of_driver-1]:
            #     if D[part_id_of_driver+245-1][int(i)+245-1] <= driver.area_finding:
            #         partition_in_range.append(i)
            # # 找到要求范围内，热门指数最大的区域
            # max_hot_index_partition = partitions[int(partition_in_range[0])-1]
            # for i in range(1,len(partition_in_range)):
            #     if partitions[int(partition_in_range[i])-1].hot_index > max_hot_index_partition.hot_index:
            #         max_hot_index_partition = partitions[int(partition_in_range[i])-1]
            next_partition = partitions[random.randint(0,174)]

            driver.route.extend(
                (str(driver.cur_location) + obtainPath(
                    driver.cur_location - 1, next_partition.partition_id + 245 - 1) + str(
                    next_partition.partition_id + 245)).split())
            del driver.route[0]
            # print(driver.route)

D = np.loadtxt('dist.txt')
T = np.loadtxt('time.txt')
Gt = np.loadtxt('Gt.txt')
Gd = np.loadtxt('Gd.txt')