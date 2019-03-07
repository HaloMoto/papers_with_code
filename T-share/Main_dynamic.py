#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Timeframe
from Algorithm import *

starttime = Timeframe.starttime
endtime = Timeframe.endtime

num_of_drivers = input('Please enter the number of drivers:')
num_of_querys = input('How many queries per one second on average:')

driver_list = []
query_list = []

for i in range(int(num_of_drivers)):
    driver_list.append(Driver(i))

query_id = 1

while endtime <= Timeframe.untildatetime:
    for i in range(int(num_of_querys)):
        query_list.append(Query(query_id,starttime))
        query_id = query_id + 1
    print(len(query_list))
    # print(query_list)
    for query in query_list:
        satisfied_driver_list = dual_side_search(driver_list, query, starttime)
        # print(len(satisfied_driver_list))
        # for driver in satisfied_driver_list:
        #     print(driver.driver_id)
        for j in range(len(satisfied_driver_list)):
            # if not satisfied_driver_list[j].cur_schedule:
            #     if insertion_feasibility_check(query_list[i], satisfied_driver_list[j], 1, 1, 0):
            #         num_of_satisfied_query = num_of_satisfied_query + 1
            #         break
            # If schedule is empty, insert it directly.
            if not satisfied_driver_list[j].cur_schedule:
                satisfied_driver_list[j].cur_schedule.append([query.source, query.pickup_window[1], 0])
                satisfied_driver_list[j].route.extend(
                    (str(get_which_grid_the_location_belongs_to(satisfied_driver_list[j].cur_location)) + obtainPath(
                        get_which_grid_the_location_belongs_to(satisfied_driver_list[j].cur_location) - 1,
                        get_which_grid_the_location_belongs_to(query.source) - 1) + str(
                        get_which_grid_the_location_belongs_to(query.source))).split())
                satisfied_driver_list[j].cur_schedule.append([query.destination, query.delivery_window[1], 1])
                satisfied_driver_list[j].route.extend(
                    (str(get_which_grid_the_location_belongs_to(query.source)) + obtainPath(
                        get_which_grid_the_location_belongs_to(query.source) - 1,
                        get_which_grid_the_location_belongs_to(query.destination) - 1) + str(
                        get_which_grid_the_location_belongs_to(query.destination))).split())
                satisfied_driver_list[j].add_passenger(1)
                query_list.remove(query)
                break

            for m in range(1, int(len(satisfied_driver_list[j].cur_schedule))+1):
                for n in range(m,int(len(satisfied_driver_list[j].cur_schedule))+2):
                    if insertion_feasibility_check(query, satisfied_driver_list[j], m, n, starttime):
                        # print('hello')
                        query_list.remove(query)
                        break
                else:
                    continue
                break
            else:
                continue
            break


    for i in range(int(num_of_drivers)):
        if driver_list[i].cur_schedule:
            print(driver_list[i].cur_schedule)

    # Refresh the location of drivers
    for driver in driver_list:
        driver.reach_the_next_point((endtime-starttime).seconds)

    # Delete expired queries
    for query in query_list:
        if endtime > query.pickup_window[1]:
            query_list.remove(query)

    starttime = endtime
    endtime = endtime + Timeframe.windowsize