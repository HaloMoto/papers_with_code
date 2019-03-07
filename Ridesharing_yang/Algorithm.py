#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Driver import Driver
from Query import Query
from functools import cmp_to_key
import numpy as np
from Auxiliary import obtainPath
import datetime
import pickle

# Load partitions
with open('partitions.txt','rb') as f:
    partitions = pickle.load(f)

# Load nodes_belong_to_which_partition.txt
with open('nodes_belong_to_which_partition.txt','rb') as f:
    nodes_belong_to_which_partition = pickle.load(f)

def empty_driver_search(driver_list, query, t_cur):
    part_id = nodes_belong_to_which_partition[query.pickup_location]
    partitions_selected = []
    empty_driver_list = []
    # Gt从下标0开始partition 1
    for i in range(len(Gt[part_id-1])):
        if t_cur + datetime.timedelta(seconds=T[part_id-1+245][int(Gt[part_id-1][i])-1+245]) <= query.latest_pickup_time:
            partitions_selected.append(part_id)
        else:
            break
    # 取出区域内的所有司机
    for part_id_temp in partitions_selected:
        for driver in driver_list:
            if nodes_belong_to_which_partition[driver.cur_location] == part_id_temp and driver.num_of_occupied_position == 0:
                empty_driver_list.append(driver)

    # 按照司机到接应点的距离由近及远进行排序
    empty_driver_list.sort(key=cmp_to_key(lambda driver1,driver2: D[query.pickup_location-1,driver1.cur_location-1]-D[query.pickup_location-1,driver2.cur_location-1]))

    return empty_driver_list


def one_passenger_driver_search(driver_list, query, t_cur):
    part_id = nodes_belong_to_which_partition[query.pickup_location]
    partitions_selected = []
    one_passenger_driver_list = []
    # Gt从下标0开始partition 1
    for i in range(len(Gt[part_id - 1])):
        if t_cur + datetime.timedelta(seconds=T[part_id - 1 + 245][int(Gt[part_id-1][i]) - 1 + 245]) <= query.latest_pickup_time:
            partitions_selected.append(part_id)
        else:
            break
    # 取出区域内的所有司机
    for part_id_temp in partitions_selected:
        for driver in driver_list:
            if nodes_belong_to_which_partition[driver.cur_location] == part_id_temp and driver.num_of_occupied_position == 1:
                one_passenger_driver_list.append(driver)

    # 按照司机到接应点的距离由近及远进行排序
    one_passenger_driver_list.sort(key=cmp_to_key(
        lambda driver1, driver2: D[query.pickup_location - 1, driver1.cur_location - 1] - D[
            query.pickup_location - 1, driver2.cur_location - 1]))

    return one_passenger_driver_list

def two_passenger_driver_search(driver_list, query, t_cur):
    part_id = nodes_belong_to_which_partition[query.pickup_location]
    partitions_selected = []
    two_passenger_driver_list = []
    # Gt从下标0开始partition 1
    for i in range(len(Gt[part_id - 1])):
        if t_cur + datetime.timedelta(seconds=T[part_id - 1 + 245][int(Gt[part_id-1][i]) - 1 + 245]) <= query.latest_pickup_time:
            partitions_selected.append(part_id)
        else:
            break
    # 取出区域内的所有司机
    for part_id_temp in partitions_selected:
        for driver in driver_list:
            if nodes_belong_to_which_partition[
                driver.cur_location] == part_id_temp and driver.num_of_occupied_position == 2:
                two_passenger_driver_list.append(driver)

    # 按照司机到接应点的距离由近及远进行排序
    two_passenger_driver_list.sort(key=cmp_to_key(
        lambda driver1, driver2: D[query.pickup_location - 1, driver1.cur_location - 1] - D[
            query.pickup_location - 1, driver2.cur_location - 1]))

    return two_passenger_driver_list

def three_passenger_driver_search(driver_list, query, t_cur):
    part_id = nodes_belong_to_which_partition[query.pickup_location]
    partitions_selected = []
    three_passenger_driver_list = []
    # Gt从下标0开始partition 1
    for i in range(len(Gt[part_id - 1])):
        if t_cur + datetime.timedelta(seconds=T[part_id - 1 + 245][int(Gt[part_id-1][i]) - 1 + 245]) <= query.latest_pickup_time:
            partitions_selected.append(part_id)
        else:
            break
    # 取出区域内的所有司机
    for part_id_temp in partitions_selected:
        for driver in driver_list:
            if nodes_belong_to_which_partition[
                driver.cur_location] == part_id_temp and driver.num_of_occupied_position == 3:
                three_passenger_driver_list.append(driver)

    # 按照司机到接应点的距离由近及远进行排序
    three_passenger_driver_list.sort(key=cmp_to_key(
        lambda driver1, driver2: D[query.pickup_location - 1, driver1.cur_location - 1] - D[
            query.pickup_location - 1, driver2.cur_location - 1]))

    return three_passenger_driver_list

def insertion_feasibility_check(query, driver, m, n, t_cur):
    # Calculate the time from driver.cur_location to query.pickup_location
    t_i = 0
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
    for i in range(m,len(driver.cur_schedule)-1):
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
        if m == 1 and driver.cur_schedule[0][0] == driver.cur_schedule[1][0]:
            driver.assist_t = 0

        return True

    #Check the time delay incurred by the insertion of query.source causes the slack time of any point after position i in schedule V.s smaller than 0
    t_j = t_j + T[query.delivery_location-1][driver.cur_schedule[n+1-1][0]-1]
    if t_cur + datetime.timedelta(seconds=t_j) > driver.cur_schedule[n+1-1][1]:
        del driver.cur_schedule[m-1]
        return False
    for j in range(n+1, len(driver.cur_schedule)-1):
        t_j = t_j + T[driver.cur_schedule[j-1][0]-1][driver.cur_schedule[j][0]-1]
        if t_cur + datetime.timedelta(seconds=t_j) > driver.cur_schedule[j][1]:
            del driver.cur_schedule[m-1]
            return False
    driver.cur_schedule.insert(n + 1 - 1, [query.delivery_location, query.latest_delivery_time, 1]) # Insert query.delivery_location into driver.cur_schedule as position n

    driver.add_passenger(1)

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
    if m == 1 and driver.cur_schedule[0][0] == driver.cur_schedule[1][0]:
        driver.assist_t = 0

    return True


def recommendation(driver_list):
    for driver in driver_list:
        if driver.num_of_occupied_position == 0 and not driver.route:
            part_id_of_driver = nodes_belong_to_which_partition[driver.cur_location]
            partition_in_range = []
            for i in Gd[part_id_of_driver-1]:
                if D[part_id_of_driver+245-1][int(i)+245-1] <= driver.area_finding:
                    partition_in_range.append(i)
            # 找到要求范围内，热门指数最大的区域
            max_hot_index_partition = partitions[int(partition_in_range[0])-1]
            for i in range(1,len(partition_in_range)):
                if partitions[int(partition_in_range[i])-1].hot_index > max_hot_index_partition.hot_index:
                    max_hot_index_partition = partitions[int(partition_in_range[i])-1]

            driver.route.extend(
                (str(driver.cur_location) + obtainPath(
                    driver.cur_location - 1, max_hot_index_partition.partition_id + 245 - 1) + str(
                    max_hot_index_partition.partition_id + 245)).split())

            # print(driver.route)

D = np.loadtxt('dist.txt')
T = np.loadtxt('time.txt')
Gt = np.loadtxt('Gt.txt')
Gd = np.loadtxt('Gd.txt')