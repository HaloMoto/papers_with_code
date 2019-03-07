#!/usr/bin/python
# -*- coding: utf-8 -*-

from Auxiliary import get_which_grid_the_location_belongs_to
from Driver import Driver
from Query import Query
from functools import cmp_to_key
import numpy as np
from Auxiliary import obtainPath
import sys
import datetime

def dual_side_search(driver_list, query, t_cur):
    g_o = query.source
    S_o = list(filter(lambda driver: t_cur + datetime.timedelta(seconds=T[get_which_grid_the_location_belongs_to(g_o)-1, get_which_grid_the_location_belongs_to(driver.cur_location)-1])<=query.pickup_window[1],driver_list))
    S_o.sort(key=cmp_to_key(lambda driver1,driver2: D[get_which_grid_the_location_belongs_to(g_o)-1,get_which_grid_the_location_belongs_to(driver1.cur_location)-1]-D[get_which_grid_the_location_belongs_to(g_o)-1,get_which_grid_the_location_belongs_to(driver2.cur_location)-1]))
    # print(S_o)
    g_d = query.destination
    S_d = list(filter(lambda driver: t_cur + datetime.timedelta(seconds=T[get_which_grid_the_location_belongs_to(g_d)-1, get_which_grid_the_location_belongs_to(driver.cur_location)-1])<=query.delivery_window[1],driver_list))
    S_d.sort(key=cmp_to_key(lambda driver1, driver2: D[get_which_grid_the_location_belongs_to(g_d)-1, get_which_grid_the_location_belongs_to(driver1.cur_location)-1] - D[get_which_grid_the_location_belongs_to(g_d)-1, get_which_grid_the_location_belongs_to(driver2.cur_location)-1]))
    # print(S_d)
    S_intersection = list(set(S_o).intersection(set(S_d)))
    # print("1")
    l_o = []
    # for g_i in Gt[get_which_grid_the_location_belongs_to(g_o)]:
    #     if g_i == 400:
    #         print(int(g_i))
    for g_i in Gt[get_which_grid_the_location_belongs_to(g_o)-1]:
        if t_cur + datetime.timedelta(seconds=T[get_which_grid_the_location_belongs_to(g_o)-1][int(g_i)-1]) <= query.pickup_window[1]:
            l_o.append(g_i)
        else:
            break

    # print("2")
    l_d = []
    for g_j in Gt[get_which_grid_the_location_belongs_to(g_d)-1]:
        if t_cur + datetime.timedelta(seconds=T[get_which_grid_the_location_belongs_to(g_d)-1][int(g_j)-1]) <= query.delivery_window[1]:
            l_d.append(g_j)
        else:
            break;

    stop_o = False
    stop_d = False
    # print("3")
    while S_intersection and (stop_o == False or stop_d == False):
        if l_o:
            g_i = l_o.pop(0)
            S_o = list(set(S_o).union(set(list(filter(lambda driver: T[int(g_i) - 1, get_which_grid_the_location_belongs_to(driver.cur_location) - 1] <= (query.pickup_window[1]-t_cur).seconds,driver_list)))))
            S_o.sort(key=cmp_to_key(lambda driver1, driver2: D[int(g_i) - 1, get_which_grid_the_location_belongs_to(driver1.cur_location) - 1] - D[int(g_i) - 1, get_which_grid_the_location_belongs_to(driver2.cur_location) - 1]))
        else:
            stop_o = True
        if l_d:
            g_j = l_d.pop(0)
            S_d = list(set(S_d).union(set(list(filter(lambda driver: T[int(g_j) - 1, get_which_grid_the_location_belongs_to(driver.cur_location) - 1] <= (query.delivery_window[1]-t_cur).seconds,driver_list)))))
            S_d.sort(key=cmp_to_key(lambda driver1, driver2: D[int(g_j) - 1, get_which_grid_the_location_belongs_to(driver1.cur_location) - 1] - D[int(g_j) - 1, get_which_grid_the_location_belongs_to(driver2.cur_location) - 1]))
        else:
            stop_d = True
        S_intersection = list(set(S_o).intersection(set(S_d)))

    return S_intersection

def insertion_feasibility_check(query, driver, m, n, t_cur):
    # No remaining seats
    if driver.num_of_occupied_position == Driver.capacity:
        return False

    # Calculate the time from driver.cur_location to query.source
    t_i = 0
    t_i = t_i + T[get_which_grid_the_location_belongs_to(driver.cur_location)-1][get_which_grid_the_location_belongs_to(driver.cur_schedule[0][0])-1]
    for i in range(m-2):
        t_i = t_i + T[get_which_grid_the_location_belongs_to(driver.cur_schedule[i][0])-1][get_which_grid_the_location_belongs_to(driver.cur_schedule[i+1][0])-1]
    t_i = t_i + T[get_which_grid_the_location_belongs_to(driver.cur_schedule[m-2][0])-1][get_which_grid_the_location_belongs_to(query.source)-1]

    if t_cur + datetime.timedelta(seconds=t_i) > query.pickup_window[1]:
        return False

    # Check the time delay incurred by the insertion of query.source causes the slack time of any point after position i in schedule V.s smaller than 0
    t_i = t_i + T[get_which_grid_the_location_belongs_to(query.source)-1][get_which_grid_the_location_belongs_to(driver.cur_schedule[m-1][0])-1]
    if t_cur + datetime.timedelta(seconds=t_i) > driver.cur_schedule[m-1][1]:
        return False
    for i in range(m,len(driver.cur_schedule)-1):
        t_i = t_i + T[get_which_grid_the_location_belongs_to(driver.cur_schedule[i-1][0])-1][get_which_grid_the_location_belongs_to(driver.cur_schedule[i][0])-1]
        if t_cur + datetime.timedelta(seconds=t_i) > driver.cur_schedule[i][1]:
            return False
    driver.cur_schedule.insert(m-1, [query.source,query.pickup_window[1], 0]) # Insert query.source into driver.cur_schedule at position m

    # Calculate the time from driver.cur_location to query.destination
    t_j = 0
    t_j = t_j + T[get_which_grid_the_location_belongs_to(driver.cur_location)-1][get_which_grid_the_location_belongs_to(driver.cur_schedule[0][0])-1]
    for j in range(n + 1 - 2):
        t_j = t_j + T[get_which_grid_the_location_belongs_to(driver.cur_schedule[j][0])-1][
            get_which_grid_the_location_belongs_to(driver.cur_schedule[j + 1][0])-1]
    t_j = t_j + T[get_which_grid_the_location_belongs_to(driver.cur_schedule[n + 1 - 2][0])-1][
        get_which_grid_the_location_belongs_to(query.destination)-1]

    if t_cur + datetime.timedelta(seconds=t_j) > query.delivery_window[1]:
        del driver.cur_schedule[m-1]
        return False

    # Check the time delay incurred by the insertion of query.source causes the slack time of any point after position i in schedule V.s smaller than 0
    t_j = t_j + T[get_which_grid_the_location_belongs_to(query.destination)-1][get_which_grid_the_location_belongs_to(driver.cur_schedule[n+1-1][0])-1]
    if t_cur + datetime.timedelta(seconds=t_j) > driver.cur_schedule[n+1-1][1]:
        del driver.cur_schedule[m - 1]
        return False
    for j in range(n+1,len(driver.cur_schedule)-1):
        t_j = t_j + T[get_which_grid_the_location_belongs_to(driver.cur_schedule[j-1][0])-1][get_which_grid_the_location_belongs_to(driver.cur_schedule[j][0])-1]
        if t_cur + datetime.timedelta(seconds=t_j) > driver.cur_schedule[j][1]:
            del driver.cur_schedule[m - 1]
            return False
    driver.cur_schedule.insert(n + 1 - 1, [query.destination, query.delivery_window[1], 1])  # Insert query.destination into driver.cur_schedule at position n

    driver.add_passenger(1)
    # Recalculate route after schedule change
    driver.route.extend((str(get_which_grid_the_location_belongs_to(driver.cur_schedule[-3][0])) + obtainPath(
        get_which_grid_the_location_belongs_to(driver.cur_schedule[-3][0]) - 1,
        get_which_grid_the_location_belongs_to(driver.cur_schedule[-2][0]) - 1) + str(
        get_which_grid_the_location_belongs_to(driver.cur_schedule[-2][0]))).split())
    driver.route.extend((str(get_which_grid_the_location_belongs_to(driver.cur_schedule[-2][0])) + obtainPath(
        get_which_grid_the_location_belongs_to(driver.cur_schedule[-2][0]) - 1,
        get_which_grid_the_location_belongs_to(driver.cur_schedule[-1][0]) - 1) + str(
        get_which_grid_the_location_belongs_to(driver.cur_schedule[-1][0]))).split())
    # print('world')
    return True

D = np.loadtxt('dist.txt')
T = np.loadtxt('time.txt')
Gt = np.loadtxt('Gt.txt')

################################
#            Test1
################################
# driver_list = []
# for i in range(500):
#     driver_list.append(Driver(i))
# query = Query(1)
# # print(dual_side_search(driver_list, query))
# starttime = datetime.datetime.now()
# S = dual_side_search(driver_list, query, 0)
# for i in range(len(S)):
#     print(S[i].cur_location)
# print("query:",query.source)
#
# for driver in S:
#     if insertion_feasibility_check(query, driver, 1, 2, 0):
#         print("driver id:", driver.driver_id)
#         print(driver.cur_schedule)
#         break
#
# endtime = datetime.datetime.now()
#
# print((endtime-starttime).seconds)