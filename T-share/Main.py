#!/usr/bin/python
# -*- coding: utf-8 -*-

from Driver import Driver
from Query import Query
from Algorithm import *

num_of_drivers = input('Please enter the number of drivers:')
num_of_querys = input('Please enter the number of querys:')

driver_list = []
query_list = []
num_of_satisfied_query = 0

for i in range(int(num_of_drivers)):
    driver_list.append(Driver(i))

for i in range(int(num_of_querys)):
    query_list.append(Query(i))

for i in range(int(num_of_querys)):
    print(i)
    satisfied_driver_list = dual_side_search(driver_list, query_list[i], 0)
    # for driver in satisfied_driver_list:
    #     print(driver.driver_id)
    for j in range(len(satisfied_driver_list)):
        # if not satisfied_driver_list[j].cur_schedule:
        #     if insertion_feasibility_check(query_list[i], satisfied_driver_list[j], 1, 1, 0):
        #         num_of_satisfied_query = num_of_satisfied_query + 1
        #         break
        for m in range(1,int(len(satisfied_driver_list[j].cur_schedule)/2)+2):
            for n in range(int(len(satisfied_driver_list[j].cur_schedule)/2)+1, int(len(satisfied_driver_list[j].cur_schedule))+2):
                if insertion_feasibility_check(query_list[i], satisfied_driver_list[j], m, n, 0):
                    num_of_satisfied_query = num_of_satisfied_query + 1
                    break
            else: continue
            break
        else: continue
        break

print("number of satisfied query:", num_of_satisfied_query)
for i in range(int(num_of_drivers)):
    if driver_list[i].cur_schedule:
        print(driver_list[i].cur_schedule)

#############################
#         Test2
#############################
# print(driver_list[0])
# print(passenger_list[1])

#############################
#         Test1
#############################
# print(num_of_drivers, num_of_passengers)