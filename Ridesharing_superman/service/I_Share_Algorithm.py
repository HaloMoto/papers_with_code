#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime
from service.Auxiliary import obtainPath
from math import ceil
from scipy.cluster.vq import kmeans2
from functools import cmp_to_key
import config.Timeframe as Timeframe
from bean.Cluster import Cluster
import pickle
from math import floor, ceil, factorial, exp

## 文件载入 ##
D = np.loadtxt('../data/dist.txt')
T = np.loadtxt('../data/time.txt')
Gt = np.loadtxt('../data/Gt.txt')
Gd = np.loadtxt('../data/Gd.txt')
LQ = np.loadtxt('../data/location_query.txt')
Gt_c = np.loadtxt('../data/Gt_c.txt')
Gd_c = np.loadtxt('../data/Gd_c.txt')
# 节点所属格子
with open('../data/nodes_belong_to_which_grid.txt', "rb") as f:
    nodes_belong_to_which_grid = pickle.load(f)

with open("../data/node_all.txt","r") as file_to_read:
    # 从文件中读取十字路口数
    num_of_intersections = int(file_to_read.readline())
    # 从文件中读取格子数
    num_of_grids = int(file_to_read.readline())
    # 从文件中读取聚类数
    num_of_clusters = int(file_to_read.readline())

## 拼单算法
def combination_of_multiple_orders(query_list, regl_Hexg_grids, driver_list, t_cur):
    ## 统计订单的传送点所在区域，并将统计结果保存入字典中
    # 字典定义
    dict_of_delivery_point_belongs_to = dict()
    # 以区域id作为key，value为列表（保存订单）
    for i in range(num_of_clusters):
        dict_of_delivery_point_belongs_to[i+1] = []
    for query in query_list:
        for i in regl_Hexg_grids[query.delivery_location-num_of_intersections-1].delivery_cluster:
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
            is_successful = find_the_nearest_empty_car_for_many(regl_Hexg_grids, merged_order, driver_list, t_cur)
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
                        is_successful = find_the_nearest_empty_car_for_many(regl_Hexg_grids, merged_order, driver_list, t_cur)
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
                            is_successful = find_the_nearest_empty_car_for_many(regl_Hexg_grids, merged_orders[j], driver_list, t_cur)
                            ## 如果找到了空车，那么改订单状态为已服务
                            if is_successful:
                                for query in merged_orders[j]:
                                    query.condition = 1

## 订单插入检查 ##
def insertion_feasibility_check(query, driver, m, n, t_cur, regl_Hexg_grids):
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
        # 从格子的driver_will_coming中删除剩下路径
        for node in driver.route:
            regl_Hexg_grids[nodes_belong_to_which_grid[node]-1].driver_will_coming = [driver_tuple for driver_tuple in regl_Hexg_grids[nodes_belong_to_which_grid[node]-1].driver_will_coming if driver_tuple[0] != driver.driver_id]
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
        # 遍历司机的路径列表
        for node_will_pass in driver.route:
            node_will_pass = int(node_will_pass)
            regl_Hexg_grids[nodes_belong_to_which_grid[node_will_pass] - 1].driver_will_coming.append(
                [driver.driver_id,
                 t_cur + datetime.timedelta(seconds=T[driver.cur_location - 1][node_will_pass - 1])])
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
    # 从格子的driver_will_coming中删除剩下路径
    for node in driver.route:
        regl_Hexg_grids[nodes_belong_to_which_grid[node] - 1].driver_will_coming = [driver_tuple for driver_tuple in
                                                                                    regl_Hexg_grids[
                                                                                        nodes_belong_to_which_grid[
                                                                                            node] - 1].driver_will_coming
                                                                                    if
                                                                                    driver_tuple[0] != driver.driver_id]
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
    # 遍历司机的路径列表
    for node_will_pass in driver.route:
        node_will_pass = int(node_will_pass)
        regl_Hexg_grids[nodes_belong_to_which_grid[node_will_pass] - 1].driver_will_coming.append(
            [driver.driver_id,
             t_cur + datetime.timedelta(seconds=T[driver.cur_location - 1][node_will_pass - 1])])
    # 如果改变路径前后，下一个点相同，那么assist_t不变，否则变为-abs(driver.assist_t)
    if driver.route[0] == first_location_origin_route:
        driver.assist_t = driver.assist_t
    else:
        driver.assist_t = -abs(driver.assist_t)

    return True

## 为合单寻找一辆空车
def find_the_nearest_empty_car_for_many(regl_Hexg_grids, merged_order, driver_list, t_cur):
    # 找出latest_pickup_time最小的订单
    merged_order.sort(key=lambda query:query.latest_pickup_time)
    # 为合单的每一个订单的接载点初始化一个保存格子的字典集合
    L_os = dict()
    for i in range(len(merged_order)):
        L_os[i] = []
    # 寻找距离所有订单所在格子最近的格子
    for i in range(len(merged_order)):
        for g_i in Gt[merged_order[i].pickup_location-num_of_intersections-1]:
            if t_cur + datetime.timedelta(
                    seconds=T[merged_order[i].pickup_location - 1][int(g_i) + num_of_intersections - 1]) <= merged_order[i].latest_pickup_time:
                L_os[i].append(g_i)
            else:
                break
    # 求多个list的交集
    # 初始化交集列表
    S_intersection = [grid for grid in L_os[0] if grid in L_os[1]]
    for i in range(2, len(merged_order)):
        S_intersection = [grid for grid in S_intersection if grid in L_os[i]]
    ## 判断集合是否为空
    if S_intersection:
        return False
    else:
        # 集合不为空，从集合中选出格子，然后从格子中找出空车司机
        for grid in S_intersection:
            for driver_tuple in regl_Hexg_grids[grid-1].driver_will_coming:
                if driver_list[driver_tuple[0]].num_of_occupied_position == 0 and driver_list[driver_tuple[1]] < merged_order[0].latest_pickup_time:
                    ## 找到空车司机
                    #进行路径规划
                    merged_order.sort(key=cmp_to_key(lambda query_1, query_2: D[grid + num_of_intersections - 1][query_1.pickup_location - 1] - D[grid + num_of_intersections - 1][query_2.pickup_location - 1]))
                    # 将订单中的接应点加入到司机安排中
                    for query in merged_order:
                        driver_list[driver_tuple[0]].cur_schedule.append([query.pickup_location, query.latest_pickup_time, 0])
                    ## 将订单根据接应点进行排序
                    merged_order.sort(key=cmp_to_key(
                        lambda query_1, query_2: D[grid + num_of_intersections - 1][query_1.delivery_location - 1] -
                                                 D[grid + num_of_intersections - 1][query_2.delivery_location - 1]))
                    # 将订单中的接应点加入到司机安排中
                    for query in merged_order:
                        driver_list[driver_tuple[0]].cur_schedule.append(
                            [query.delivery_location, query.latest_delivery_time, 1])
                    # 路径规划
                    # 乘客加len(merged_order)
                    driver_list[driver_tuple[0]].add_passenger(len(merged_order))
                    # 原来路径的第一个点
                    first_location_origin_route = driver_list[driver_tuple[0]].route[0]
                    # 从格子的driver_will_coming中删除剩下路径
                    for node in driver_list[driver_tuple[0]].route:
                        regl_Hexg_grids[nodes_belong_to_which_grid[node] - 1].driver_will_coming = [driver_tuple for
                                                                                                    driver_tuple in
                                                                                                    regl_Hexg_grids[
                                                                                                        nodes_belong_to_which_grid[
                                                                                                            node] - 1].driver_will_coming
                                                                                                    if
                                                                                                    driver_tuple[
                                                                                                        0] != driver_list[driver_tuple[0]].driver_id]
                    # Recalculate route after schedule change
                    driver_list[driver_tuple[0]].route = []
                    driver_list[driver_tuple[0]].route.extend(
                        (str(driver_list[driver_tuple[0]].cur_location) + obtainPath(
                            driver_list[driver_tuple[0]].cur_location - 1, driver_list[driver_tuple[0]].cur_schedule[0][0] - 1) + str(
                            driver_list[driver_tuple[0]].cur_schedule[0][0])).split())
                    for i in range(len(driver_list[driver_tuple[0]].cur_schedule) - 1):
                        driver_list[driver_tuple[0]].route.extend(
                            (obtainPath(
                                driver_list[driver_tuple[0]].cur_schedule[i][0] - 1, driver_list[driver_tuple[0]].cur_schedule[i + 1][0] - 1) + str(
                                driver_list[driver_tuple[0]].cur_schedule[i + 1][0])).split())
                    del driver_list[driver_tuple[0]].route[0]
                    # 遍历司机的路径列表
                    for node_will_pass in driver_list[driver_tuple[0]].route:
                        node_will_pass = int(node_will_pass)
                        regl_Hexg_grids[nodes_belong_to_which_grid[node_will_pass] - 1].driver_will_coming.append(
                            [driver_list[driver_tuple[0]].driver_id,
                             t_cur + datetime.timedelta(seconds=T[driver_list[driver_tuple[0]].cur_location - 1][node_will_pass - 1])])
                    # 如果调整之后的路径第一个点和原始路径第一个点相同
                    if driver_list[driver_tuple[0]].route[0] == first_location_origin_route:
                        driver_list[driver_tuple[0]].assist_t = driver_list[driver_tuple[0]].assist_t
                    else:
                        driver_list[driver_tuple[0]].assist_t = -abs(driver_list[driver_tuple[0]].assist_t)
                    #返回True
                    return True
    return False

## 双边查询算法
def dual_side_taxi_searching(driver_list, regl_Hexg_grids, query, t_cur):
    # 订单接应点
    g_o = query.pickup_location
    # 接应点所在格子内的所有司机，并从这些司机中筛选出在pickup_latest_time之前到这个格子的司机
    S_o = []
    for driver_tuple in regl_Hexg_grids[query.pickup_location-num_of_intersections-1].driver_will_coming:
        if driver_tuple[1] <= query.latest_pickup_time and driver_list[driver_tuple[0]].num_of_occupied_position != 0:
            S_o.append(driver_list[int(driver_tuple[0])-1])
    # 订单传送点
    g_d = query.delivery_location
    # 传送点所在格子内的所有司机，并从这些司机中筛选出在delivery_latest_time之前到这个格子且车上乘客数不为0的司机
    S_d = []
    for driver_tuple in regl_Hexg_grids[query.delivery_location-num_of_intersections-1].driver_will_coming:
        if driver_tuple[1] <= query.latest_delivery_time and driver_list[driver_tuple[0]].num_of_occupied_position != 0:
            S_d.append(driver_list[int(driver_tuple[0])-1])
    # S_o和S_d两个集合的交集
    S_intersection = list(set(S_o).intersection(set(S_d)))
    ## 将能在latest_pickup_time之前到达query.pickup_location所在格子的所有格子保存入一个列表中
    l_o = []
    for g_i in Gt[g_o-num_of_intersections-1]:
        if t_cur + datetime.timedelta(seconds=T[g_o-1][int(g_i)+num_of_intersections-1]) <= query.latest_pickup_time:
            l_o.append(g_i)
        else:
            break
    ## 将能在latest_delivery_time之前到达query.delivery_location所在格子的所有格子保存入一个列表中
    l_d = []
    for g_j in Gt[g_d-num_of_intersections-1]:
        if t_cur + datetime.timedelta(seconds=T[g_d-1][int(g_j)+num_of_intersections-1]) <= query.latest_delivery_time:
            l_d.append(g_j)
        else:
            break
    ## 一些判断标志
    stop_o = False
    stop_d = False
    while not S_intersection and (stop_o == False or stop_d == False):
        if l_o:
            # 获得最近的一个格子
            g_i = l_o.pop(0)
            # 将格子中的司机取出来
            for driver_tuple in regl_Hexg_grids[int(g_i) - 1].driver_will_coming:
                if driver_tuple[1] <= query.latest_pickup_time and driver_list[driver_tuple[0]].num_of_occupied_position != 0:
                    S_o.append(driver_list[int(driver_tuple[0]) - 1])
        else:
            stop_o = True
        if l_d:
            # 获得最近的一个格子
            g_j = l_d.pop(0)
            # 将格子中的司机取出来
            for driver_tuple in regl_Hexg_grids[int(g_j)-1].driver_will_coming:
                if driver_tuple[1] <= query.latest_delivery_time and driver_list[driver_tuple[0]].num_of_occupied_position != 0:
                    S_d.append(driver_list[int(driver_tuple[0])-1])
        else:
            stop_d = False
        # 取交集
        S_intersection = list(set(S_o).intersection(set(S_d)))
    ## 遍历查询结果
    for j in range(len(S_intersection)):
        for m in range(1, int(len(S_intersection[j].cur_schedule))+1):
            for n in range(m, int(len(S_intersection[j].cur_schedule))+2):
                if insertion_feasibility_check(query, S_intersection[j], m, n, t_cur, regl_Hexg_grids):
                    # 插入成功，改变订单状态为已服务
                    query.condition = 1
                    # 司机接的订单数加一
                    S_intersection[j].number_of_order += 1
                    break
            else:
                continue
            break
        else:
            continue
        break

## 推荐算法
def recommendation(driver_list, pickup_clusters, t_cur, regl_Hexg_grids, amplification_factor):
    ## 预测模型参数
    a = 1
    b = 3/4
    c = 2/4
    d = 1/4
    ## 给空车司机推荐路径
    for driver in driver_list:
        if driver.num_of_occupied_position == 0:
            ## 初始化变量
            ## 寻找到距离司机最近的区域
            nearest_cluster_id = regl_Hexg_grids[nodes_belong_to_which_grid[driver.cur_location]-1].pickup_cluster[0]
            ## 到达最近区域所需要的时间
            t_go = T[driver.cur_location-1][num_of_intersections+num_of_grids+nearest_cluster_id-1]
            ## 司机到达最近区域所在的时间段
            time_slot = int(((t_cur - Timeframe.starttime).seconds + t_go) / 60 / Cluster.dt) + 1
            # 第time_slot段时间的开始时间
            starttime_temp = Timeframe.starttime + datetime.timedelta(seconds=(time_slot-1)*60*Cluster.dt)
            ## 统计当前时间以及在当前时间过后的t_go时间内，会有多少个空车司机、一个乘客司机、两个乘客司机、三个乘客司机
            # 空车司机
            empty_car = set()
            # 一个乘客司机
            one_passenger_car = set()
            # 两个乘客司机数
            two_passenger_car = set()
            # 三个乘客司机数
            three_passenger_car = set()
            ## 统计区域内所有格子的空车司机、一个乘客司机。。
            for grid in pickup_clusters[nearest_cluster_id-1].grids_included:
                for driver_tuple in regl_Hexg_grids[grid-1].driver_will_coming:
                    # 司机到达该点时间之前
                    if driver_tuple[1] < t_cur + datetime.timedelta(seconds=t_go) and driver_tuple[1] >= starttime_temp:
                        # 空车司机
                        if driver_list[driver_tuple[0]].num_of_occupied_position == 0:
                            empty_car.add(driver_tuple[0])
                        elif driver_list[driver_tuple[0]].num_of_occupied_position == 1:
                            one_passenger_car.add(driver_tuple[0])
                        elif driver_list[driver_tuple[0]].num_of_occupied_position == 2:
                            two_passenger_car.add(driver_tuple[0])
                        elif driver_list[driver_tuple[0]].num_of_occupied_position == 3:
                            three_passenger_car.add(driver_tuple[0])
                    elif driver_tuple[1] > t_cur + datetime.timedelta(seconds=t_go):
                        break
            ## 计算在当前时间到当前时间之后t_go时间内司机带走多少乘客
            num_of_passengers_taken_away = floor(a*len(empty_car)+b*len(one_passenger_car)+c*len(two_passenger_car)+d*len(three_passenger_car))
            ## t_go有多少个单位时间
            num_unit_time = ceil(t_go / Timeframe.windowsize.seconds)
            # 该区域顾客到达速率
            V_arrival = pickup_clusters[nearest_cluster_id-1].avg_of_each_duration[time_slot - 1] / (Cluster.dt * 60) * Timeframe.windowsize.seconds
            # 对区域顾客到达速率进行放大
            V_arrival = V_arrival * amplification_factor
            ## 到达num_of_passengers_taken_away+1个司机的概率
            P_max = exp(-V_arrival*num_unit_time)*pow(V_arrival*num_unit_time, num_of_passengers_taken_away+1) / factorial(num_of_passengers_taken_away+1)
            ## 最大化概率的区域
            cluster_id_max = nearest_cluster_id
            for cluster_id in Gt_c[nearest_cluster_id-1]:
                ## 到达最近区域所需要的时间
                t_go = T[driver.cur_location - 1][num_of_intersections + num_of_grids + int(cluster_id) - 1]
                ## 司机到达最近区域所在的时间段
                time_slot = int(((t_cur - Timeframe.starttime).seconds + t_go) / 60 / Cluster.dt) + 1
                # 第time_slot段时间的开始时间
                starttime_temp = Timeframe.starttime + datetime.timedelta(seconds=(time_slot - 1) * 60 * Cluster.dt)
                ## 统计当前时间以及在当前时间过后的t_go时间内，会有多少个空车司机、一个乘客司机、两个乘客司机、三个乘客司机
                # 空车司机
                empty_car = set()
                # 一个乘客司机
                one_passenger_car = set()
                # 两个乘客司机数
                two_passenger_car = set()
                # 三个乘客司机数
                three_passenger_car = set()
                ## 统计区域内所有格子的空车司机、一个乘客司机。。
                for grid in pickup_clusters[int(cluster_id) - 1].grids_included:
                    for driver_tuple in regl_Hexg_grids[grid - 1].driver_will_coming:
                        # 司机到达该点时间之前
                        if driver_tuple[1] < t_cur + datetime.timedelta(seconds=t_go) and driver_tuple[
                            1] >= starttime_temp:
                            # 空车司机
                            if driver_list[driver_tuple[0]].num_of_occupied_position == 0:
                                empty_car.add(driver_tuple[0])
                            elif driver_list[driver_tuple[0]].num_of_occupied_position == 1:
                                one_passenger_car.add(driver_tuple[0])
                            elif driver_list[driver_tuple[0]].num_of_occupied_position == 2:
                                two_passenger_car.add(driver_tuple[0])
                            elif driver_list[driver_tuple[0]].num_of_occupied_position == 3:
                                three_passenger_car.add(driver_tuple[0])
                        elif driver_tuple[1] > t_cur + datetime.timedelta(seconds=t_go):
                            break
                ## 计算在当前时间到当前时间之后t_go时间内司机带走多少乘客
                num_of_passengers_taken_away = floor(
                    a * len(empty_car) + b * len(one_passenger_car) + c * len(two_passenger_car) + d * len(
                        three_passenger_car))
                ## t_go有多少个单位时间
                num_unit_time = ceil(t_go / Timeframe.windowsize.seconds)
                # 该区域顾客到达速率
                V_arrival = pickup_clusters[int(cluster_id) - 1].avg_of_each_duration[time_slot - 1] / (
                            Cluster.dt * 60) * Timeframe.windowsize.seconds
                # 对区域顾客到达速率进行放大
                V_arrival = V_arrival * amplification_factor
                ## 到达num_of_passengers_taken_away+1个司机的概率
                P_temp = exp(-V_arrival * num_unit_time) * pow(V_arrival * num_unit_time,
                                                              num_of_passengers_taken_away + 1) / factorial(
                    num_of_passengers_taken_away + 1)
                ## 最大化概率的区域
                if P_temp > P_max:
                    P_max = P_temp
                    cluster_id_max = cluster_id
            ## 更改该司机的路径
            # 空车司机要去的区域锚点
            next_station = num_of_intersections+num_of_grids+int(cluster_id_max)
            # 路径更改
            driver.route.extend(
                (str(driver.cur_location) + obtainPath(
                    driver.cur_location - 1, next_station - 1) + str(
                    next_station)).split())
            del driver.route[0]
            # 遍历司机的路径列表
            for node_will_pass in driver.route:
                node_will_pass = int(node_will_pass)
                regl_Hexg_grids[nodes_belong_to_which_grid[node_will_pass] - 1].driver_will_coming.append([driver.driver_id, t_cur + datetime.timedelta(seconds=T[driver.cur_location - 1][node_will_pass - 1])])

## 为一单寻找一个空车司机
def find_the_nearest_empty_car_for_one(query, driver_list, regl_Hexg_grids, t_cur):
    ## 在订单的接载点所在格子寻找空车
    g_o = query.pickup_location
    # 接应点所在格子内的所有司机，并从这些司机中找出在pickup_latest_time之前到这个格子的空车司机
    for driver_tuple in regl_Hexg_grids[query.pickup_location - num_of_intersections - 1].driver_will_coming:
        if driver_tuple[1] <= query.latest_pickup_time and driver_list[driver_tuple[0]].num_of_occupied_position == 0:
            # 进行路径规划
            driver_list[driver_tuple[0]].schedule.append([query.pickup_location,query.latest_pickup_time,0])
            driver_list[driver_tuple[0]].schedule.append([query.delivery_location,query.latest_delivery_time,1])
            # 路径规划
            # 乘客加len(merged_order)
            driver_list[driver_tuple[0]].add_passenger(1)
            # 原来路径的第一个点
            first_location_origin_route = driver_list[driver_tuple[0]].route[0]
            # 从格子的driver_will_coming中删除剩下路径
            for node in driver_list[driver_tuple[0]].route:
                regl_Hexg_grids[nodes_belong_to_which_grid[node] - 1].driver_will_coming = [driver_tuple for
                                                                                            driver_tuple in
                                                                                            regl_Hexg_grids[
                                                                                                nodes_belong_to_which_grid[
                                                                                                    node] - 1].driver_will_coming
                                                                                            if
                                                                                            driver_tuple[
                                                                                                0] != driver_list[
                                                                                                driver_tuple[
                                                                                                    0]].driver_id]
            # Recalculate route after schedule change
            driver_list[driver_tuple[0]].route = []
            driver_list[driver_tuple[0]].route.extend(
                (str(driver_list[driver_tuple[0]].cur_location) + obtainPath(
                    driver_list[driver_tuple[0]].cur_location - 1,
                    driver_list[driver_tuple[0]].cur_schedule[0][0] - 1) + str(
                    driver_list[driver_tuple[0]].cur_schedule[0][0])).split())
            for i in range(len(driver_list[driver_tuple[0]].cur_schedule) - 1):
                driver_list[driver_tuple[0]].route.extend(
                    (obtainPath(
                        driver_list[driver_tuple[0]].cur_schedule[i][0] - 1,
                        driver_list[driver_tuple[0]].cur_schedule[i + 1][0] - 1) + str(
                        driver_list[driver_tuple[0]].cur_schedule[i + 1][0])).split())
            del driver_list[driver_tuple[0]].route[0]
            # 遍历司机的路径列表
            for node_will_pass in driver_list[driver_tuple[0]].route:
                node_will_pass = int(node_will_pass)
                regl_Hexg_grids[nodes_belong_to_which_grid[node_will_pass] - 1].driver_will_coming.append(
                    [driver_list[driver_tuple[0]].driver_id,
                     t_cur + datetime.timedelta(seconds=T[driver_list[driver_tuple[0]].cur_location - 1][node_will_pass - 1])])
            # 如果调整之后的路径第一个点和原始路径第一个点相同
            if driver_list[driver_tuple[0]].route[0] == first_location_origin_route:
                driver_list[driver_tuple[0]].assist_t = driver_list[driver_tuple[0]].assist_t
            else:
                driver_list[driver_tuple[0]].assist_t = -abs(driver_list[driver_tuple[0]].assist_t)
            # 成功返回True
            return True
    ## 将能在latest_pickup_time之前到达query.pickup_location所在格子的所有格子保存入一个列表中
    l_o = []
    for g_i in Gt[g_o - num_of_intersections - 1]:
        if t_cur + datetime.timedelta(
                seconds=T[g_o - 1][int(g_i) + num_of_intersections - 1]) <= query.latest_pickup_time:
            l_o.append(g_i)
        else:
            break
    ## 遍历列表l_o从中找到一个
    for g_i in l_o:
        # 将格子中的司机取出来
        for driver_tuple in regl_Hexg_grids[int(g_i) - 1].driver_will_coming:
            if driver_tuple[1] <= query.latest_pickup_time and driver_list[driver_tuple[0]].num_of_occupied_position == 0:
                # 进行路径规划
                driver_list[driver_tuple[0]].schedule.append([query.pickup_location, query.latest_pickup_time, 0])
                driver_list[driver_tuple[0]].schedule.append([query.delivery_location, query.latest_delivery_time, 1])
                # 路径规划
                # 乘客加len(merged_order)
                driver_list[driver_tuple[0]].add_passenger(1)
                # 原来路径的第一个点
                first_location_origin_route = driver_list[driver_tuple[0]].route[0]
                # 从格子的driver_will_coming中删除剩下路径
                for node in driver_list[driver_tuple[0]].route:
                    regl_Hexg_grids[nodes_belong_to_which_grid[node] - 1].driver_will_coming = [driver_tuple for
                                                                                                driver_tuple in
                                                                                                regl_Hexg_grids[
                                                                                                    nodes_belong_to_which_grid[
                                                                                                        node] - 1].driver_will_coming
                                                                                                if
                                                                                                driver_tuple[
                                                                                                    0] != driver_list[
                                                                                                    driver_tuple[
                                                                                                        0]].driver_id]
                # Recalculate route after schedule change
                driver_list[driver_tuple[0]].route = []
                driver_list[driver_tuple[0]].route.extend(
                    (str(driver_list[driver_tuple[0]].cur_location) + obtainPath(
                        driver_list[driver_tuple[0]].cur_location - 1,
                        driver_list[driver_tuple[0]].cur_schedule[0][0] - 1) + str(
                        driver_list[driver_tuple[0]].cur_schedule[0][0])).split())
                for i in range(len(driver_list[driver_tuple[0]].cur_schedule) - 1):
                    driver_list[driver_tuple[0]].route.extend(
                        (obtainPath(
                            driver_list[driver_tuple[0]].cur_schedule[i][0] - 1,
                            driver_list[driver_tuple[0]].cur_schedule[i + 1][0] - 1) + str(
                            driver_list[driver_tuple[0]].cur_schedule[i + 1][0])).split())
                del driver_list[driver_tuple[0]].route[0]
                # 遍历司机的路径列表
                for node_will_pass in driver_list[driver_tuple[0]].route:
                    node_will_pass = int(node_will_pass)
                    regl_Hexg_grids[nodes_belong_to_which_grid[node_will_pass] - 1].driver_will_coming.append(
                        [driver_list[driver_tuple[0]].driver_id,
                         t_cur + datetime.timedelta(seconds=T[driver_list[driver_tuple[0]].cur_location - 1][node_will_pass - 1])])
                # 如果调整之后的路径第一个点和原始路径第一个点相同
                if driver_list[driver_tuple[0]].route[0] == first_location_origin_route:
                    driver_list[driver_tuple[0]].assist_t = driver_list[driver_tuple[0]].assist_t
                else:
                    driver_list[driver_tuple[0]].assist_t = -abs(driver_list[driver_tuple[0]].assist_t)
                # 成功返回True
                return True
    return False