#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime
from service.Auxiliary import obtainPath
from math import ceil
from scipy.cluster.vq import kmeans2

## 文件载入 ##
D = np.loadtxt('../data/dist.txt')
T = np.loadtxt('../data/time.txt')
Gt = np.loadtxt('../data/Gt.txt')
Gd = np.loadtxt('../data/Gd.txt')
LQ = np.loadtxt('../data/location_query.txt')

with open("../data/node_all.txt","r") as file_to_read:
    # 从文件中读取十字路口数
    num_of_intersections = int(file_to_read.readline())
    # 从文件中读取格子数
    num_of_grids = int(file_to_read.readline())
    # 从文件中读取聚类数
    num_of_clusters = int(file_to_read.readline())

## 拼单算法
def combination_of_multiple_orders(query_list, regl_Hexi_grids):
    ## 统计订单的传送点所在区域，并将统计结果保存入字典中
    # 字典定义
    dict_of_delivery_point_belongs_to = dict()
    # 以区域id作为key，value为列表（保存订单）
    for i in range(num_of_clusters):
        dict_of_delivery_point_belongs_to[i+1] = []
    for query in query_list:
        for i in regl_Hexi_grids[query.delivery_location-num_of_intersections-1].delivery_cluster:
            dict_of_delivery_point_belongs_to[i].append(query)
    # 遍历字典
    for key in dict_of_delivery_point_belongs_to.keys():
        ## 首先将列表中已被服务的订单删除
        dict_of_delivery_point_belongs_to[key] = [query for query in dict_of_delivery_point_belongs_to[key] if query.condition == 0]
        if len(dict_of_delivery_point_belongs_to[key]) >= 2 and dict_of_delivery_point_belongs_to <= 4:
            ## 将该订单列表合为一单
            merged_order = dict_of_delivery_point_belongs_to[key]
            ## 寻找一辆距离最近的空车
            ## 将合并的订单分配给司机
            # 调用搜索车辆算法，返回成功 与否状态
            is_successful = find_the_nearest_empty_car(merged_order)
            ## 如果找到了空车，那么改订单状态为已服务
            if is_successful:
                for query in dict_of_delivery_point_belongs_to[key]:
                    query.condition = 1
        elif len(dict_of_delivery_point_belongs_to[key]) > 4:
            while True:
                # 使用二分K-Means算法，传入参数k
                k = ceil(len(dict_of_delivery_point_belongs_to[key])/4)
                # 将订单中传送点的经纬度地址保存到一个列表中
                coordinates = []
                for query in dict_of_delivery_point_belongs_to[key]:
                    coordinates.append(LQ[query.delivery_location-1])
                # 将coordinates列表转变为数组
                coordinates = np.array(coordinates)
                # 调用K-Means算法
                centroid, labels = kmeans2(coordinates, k, iter=20, minit='points')
                ## 获取分类结果
                # 分类结果保存字典中
                result_of_classifier = dict()
                for i in range(k):
                    result_of_classifier[i] = []
                # 将分类结果进行保存
                for i in range(len(labels)):
                     result_of_classifier[labels[i]].append(dict_of_delivery_point_belongs_to[key][i])
                # 遍历每个类别
                for i in range(k):
                    if len(result_of_classifier[i]) >= 2 and len(result_of_classifier[i]) <= 4:
                        ## 组合成一单，分配一个司机
                        ## 将该订单列表合为一单
                        merged_order = result_of_classifier[i]
                        ## 寻找一辆距离最近的空车
                        ## 将合并的订单分配给司机
                        # 调用搜索车辆算法，返回成功 与否状态
                        is_successful = find_the_nearest_empty_car(merged_order)
                        ## 如果找到了空车，那么改订单状态为已服务
                        if is_successful:
                            for query in result_of_classifier[i]:
                                query.condition = 1
                    elif len(result_of_classifier[i]) >= 5:
                        # 分配多个司机
                        num_of_drivers = ceil(len(result_of_classifier[i])/4)
                        ## avg_each_driver = int(len(result_of_classifier[i])/4)
                        ## 每个车平均avg_each_driver个订单拼成一单
                        ## 然后将剩下的订单逐一分配给前面的拼单中
                        ## 寻找num_of_drivers个司机
                        merged_orders = dict()
                        for j in range(num_of_drivers):
                            merged_orders[j] = []
                        for j in range(len(result_of_classifier[i])):
                            merged_orders[j % num_of_drivers].append(result_of_classifier[i][j])
                        ## 给每个合单分配司机
                        for j in range(num_of_drivers):
                            ## 寻找一辆距离最近的空车
                            ## 将合并的订单分配给司机
                            # 调用搜索车辆算法，返回成功 与否状态
                            is_successful = find_the_nearest_empty_car(merged_orders[j])
                            ## 如果找到了空车，那么改订单状态为已服务
                            if is_successful:
                                for query in merged_orders[j]:
                                    query.condition = 1

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

## 为合单寻找一辆空车
def find_the_nearest_empty_car(merged_order):
    pass

## 双边查询算法
def dual_side_taxi_searching(driver_list, query, t_cur):
    # 订单接应点
    g_o = query.pickup_location
    # 接应点所在格子内的所有司机，并从这些司机中筛选出在pickup_latest_time之前到这个格子的司机

    # 订单传送点
    g_d = query.delivery_location
    # 传送点所在格子内的所有司机，并从这些司机中筛选出在delivery_latest_time之前到这个格子的司机


## 推荐算法
def recommendation():
    pass