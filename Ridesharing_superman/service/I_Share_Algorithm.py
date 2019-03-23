#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime
from service.Auxiliary import obtainPath

## 文件载入 ##
D = np.loadtxt('../data/dist.txt')
T = np.loadtxt('../data/time.txt')
Gt = np.loadtxt('../data/Gt.txt')
Gd = np.loadtxt('../data/Gd.txt')

## 订单插入检查 ##
def insertion_feasibility_check(query, driver, m, n, t_cur):
    # 计算司机当前位置到达订单接载点位置所需要的时间
    t_i = 0
    # 如果m=1，那么司机直接从当前位置到达订单的接载点
    if m == 1:
        t_i = t_i + T[driver.cur_location-1][query.pickup_location-1]
    #如果m!=1，那么司机先经过schedule中前m-1个地点
    else:
        t_i = t_i + T[driver.cur_location-1][driver.cur_schedule[0][0]-1]
        for i in range(m-2):
            t_i = t_i + T[driver.cur_schedule[i][0]-1][driver.cur_schedule[i+1][0]-1]
        t_i = t_i + T[driver.cur_schedule[m-2][0]-1][query.pickup_location-1]
    # 判断到达订单接载点的时间有没有超过最晚接载时间
    if t_cur + datetime.timedelta(seconds=t_i+driver.assist_t) > query.latest_pickup_time:
        return False

    # 插入订单接载点之后，在schedule中，判断订单接载点之后的地点是否超过最晚接载时间
    t_i = t_i + T[query.pickup_location-1][driver.cur_schedule[m-1][0]-1]
    if t_cur + datetime.timedelta(seconds=t_i+driver.assist_t) > driver.cur_schedule[m-1][1]:
        return False
    for i in range(m, len(driver.cur_schedule)):
        t_i = t_i + T[driver.cur_schedule[i-1][0]-1][driver.cur_schedule[i][0]-1]
        if t_cur + datetime.timedelta(seconds=t_i+driver.assist_t) > driver.cur_schedule[i][1]:
            return False
    # 将订单接载点插入schedule中
    driver.cur_schedule.insert(m-1, [query.pickup_location, query.latest_pickup_time, 0])

    # 计算从当前位置到达订单传送点所需的时间
    t_j = 0
    t_j = t_j + T[driver.cur_location-1][driver.cur_schedule[0][0]-1]
    for j in range(n+1-2):
        t_j = t_j + T[driver.cur_schedule[j][0]-1][driver.cur_schedule[j+1][0]-1]
    t_j = t_j + T[driver.cur_schedule[n+1-2][0]-1][query.delivery_location-1]
    # 判断到达订单传送点的时间是否超过最晚传送时间
    if t_cur + datetime.timedelta(seconds=t_j+driver.assist_t) > query.latest_delivery_time:
        # 如果是，则删除插入schedule的接载点记录
        del driver.cur_schedule[m-1]
        return False
    elif n == len(driver.cur_schedule):
        # 在schedule末尾插入订单传送点
        driver.cur_schedule.insert(n+1-1, [query.delivery_location, query.latest_delivery_time, 1])
        # 车上乘客加1
        driver.add_passenger(1)
        # 原来路径的第一个点
        first_location_origin_route = driver.route[0]
        # 重新计算路径
        driver.route = []
        driver.route.extend(
            (str(driver.cur_location) + obtainPath(driver.cur_location-1, driver.cur_schedule[0][0]-1)
             + str(driver.cur_schedule[0][0])).split())
        for i in range(len(driver.cur_schedule)-1):
            driver.route.extend(
                (obtainPath(driver.cur_schedule[i][0]-1, driver.cur_schedule[i+1][0]-1) +
                 str(driver.cur_schedule[i+1][0])).split())
        # 删除当前位置
        del driver.route[0]
        # 如果调整之后的路径第一个点和原始路径第一个点相同
        if driver.route[0] == first_location_origin_route:
            driver.assist_t = driver.assist_t
        else:
            driver.assist_t = -abs(driver.assist_t)
        return True

    # 如果订单传送点插入位置不是在schedule最后，需要判断订单传送点插入位置之后的所有地点到达时是否超过最晚到达时间
    t_j = t_j + T[query.delivery_location-1][driver.cur_schedule[n+1-1][0]-1]
    if t_cur + datetime.timedelta(seconds=t_j+driver.assist_t) > driver.cur_schedule[n+1-1][1]:
        # 如果超时
        del driver.cur_schedule[m-1]
        return False
    for j in range(n+1, len(driver.cur_schedule)):
        t_j = t_j + T[driver.cur_schedule[j-1][0]-1][driver.cur_schedule[j][0]-1]
        if t_cur + datetime.timedelta(seconds=t_j+driver.assist_t) > driver.cur_schedule[j][1]:
            del driver.cur_schedule[m-1]
            return False
    # 将订单传送点插入schedule
    driver.cur_schedule.insert(n+1-1, [query.delivery_location, query.latest_delivery_time, 1])
    # 乘客加一
    driver.add_passenger(1)
    first_location_origin_route = driver.route[0]
    # 重新计算路径
    driver.route = []
    driver.route.extend(
        (str(driver.cur_location) + obtainPath(
            driver.cur_location-1, driver.cur_schedule[0][0]-1) + str(
            driver.cur_schedule[0][0])).split())
    for i in range(len(driver.cur_schedule)-1):
        driver.route.extend(
            (obtainPath(
                driver.cur_schedule[i][0]-1, driver.cur_schedule[i+1][0]-1) + str(
                driver.cur_schedule[i+1][0])).split())
    # 删除路径第一个点
    del driver.route[0]
    # 如果改变路径前后，下一个点相同，那么assist_t不变，否则变为-abs(driver.assist_t)
    if driver.route[0] == first_location_origin_route:
        driver.assist_t = driver.assist_t
    else:
        driver.assist_t = -abs(driver.assist_t)

    return True