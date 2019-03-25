#!/usr/bin/python
# -*- coding: utf-8 -*-

import config.Timeframe as Timeframe
import numpy as np
from bean.Driver import Driver
from bean.Query import Query
from bean.RHGrid import RHGrid
from bean.Cluster import Cluster
import pickle
from math import exp, factorial, pow
import random
import datetime

## 外部文件加载 ##
# 空间距离矩阵
D = np.loadtxt("../data/dist.txt")
# 时间距离矩阵
T = np.loadtxt("../data/time.txt")
# 基于所有节点的紧密性给出节点的顺序
Gd = np.loadtxt("../data/Gd.txt")
Gt = np.loadtxt("../data/Gt.txt")
# 加载格子数组数据
with open('../data/regl_Hexg_grids.txt', 'rb') as f:
    regl_Hexg_grids = pickle.load(f)
# 加载区域数组数据
with open('../data/pickup_clusters.txt', 'rb') as f:
    pickup_clusters = pickle.load(f)
with open('../data/delivery_clusters.txt', 'rb') as f:
    delivery_clusters = pickle.load(f)

with open("../data/node_all.txt","r") as file_to_read:
    # 从文件中读取十字路口数
    num_of_intersections = int(file_to_read.readline())
    # 从文件中读取格子数
    num_of_grids = int(file_to_read.readline())
    # 从文件中读取聚类数
    num_of_clusters = int(file_to_read.readline())
# 节点所属格子
with open('../data/nodes_belong_to_which_grid.txt', "rb") as f:
    nodes_belong_to_which_grid = pickle.load(f)

## 加载配置文件 ##
# 模拟开始时间
starttime = Timeframe.starttime
# 模拟结束时间
endtime = Timeframe.endtime
# 单位时间
unit_time = (starttime-endtime).seconds

## 订单分布 ##
# 顾客到达速率放大系数
amplification_factor = input('Amplification factor of arrival rate:')

## 司机数 ##
num_of_drivers = input('Please enter the number of drivers:')

## 司机池定义 ##
driver_list = []
# 订单计数器
query_id = 1

## 生成司机池, 司机id是从0开始的 ##
for i in range(int(num_of_drivers)):
    driver_list.append(Driver(i))

### 需要输入的一些模型参数 ###
# 假设每个司机接客成功率阈值相等
RSR_threshold = 0.5
# 每个区域达到多少个数（拼单阈值）进行拼单算法
RON_threshold = 10
# 单位时间内到达顾客数
num_of_arrivals = 1

### 需要输出的一些变量定义 ###
# 生成的总订单数
total_order = 0
# 被服务的订单数
number_of_order_served = 0
# 司机载客运行的总时间
total_time = 0
# 没有共享时，司机运行的总距离
total_distance = 0
# 有共享时，司机运行的总距离
total_distance_traveled = 0

### 产生订单传送点的辅助数组 ###
delivery_hot_index = []
# 时间段数目
num_of_durations = len(delivery_clusters[0].avg_of_each_duration)
# 定义辅助数组
for i in range(num_of_durations):
    delivery_hot_index.append([])
    delivery_hot_index[i].append(0)
    for cluster in delivery_clusters:
        delivery_hot_index[i].append(delivery_hot_index[i][-1] + cluster.avg_of_each_duration[i])

""" 
判断订单池中的订单数有没有超过阈值O_thres,
如果是，则订单池先经过拼单算法处理，再将剩下的订单放入搜索算法中。
如果不是，则订单直接进入搜索算法处理。将拼单算法得到的合单进行路径规划。
将搜索算法得到的合单进行插入检查 ##
"""
while endtime <= Timeframe.untildatetime:
    ## 更新每个格子的driver_will_coming列表
    for driver in driver_list:
        # 首先将已经在格子里的司机加入列表中
        regl_Hexg_grids[nodes_belong_to_which_grid[driver.cur_location] - 1].driver_will_coming.append(
            [driver.driver_id, starttime])
        # 遍历司机的路径列表
        for node_will_pass in driver.route:
            regl_Hexg_grids[nodes_belong_to_which_grid[node_will_pass] - 1].driver_will_coming.append(
                [driver.driver_id, starttime+datetime.timedelta(seconds=T[driver.cur_location-1][node_will_pass-1])])
    ## 对每个格子里的driver_will_coming列表进行排序，按照时间从早到晚排列
    for grid in regl_Hexg_grids:
        # 按照时间升序
        grid.driver_will_coming = sorted(grid.driver_will_coming, key=lambda driver: driver[1])

    ## 判断当前时间属于哪个时间段
    time_slot = (starttime - Timeframe.starttime).seconds / 60 / Cluster.dt + 1
    ## 每个单位时间，生成订单 ##
    for cluster in pickup_clusters:
        # 该区域顾客到达速率
        V_arrival = cluster.avg_of_each_duration[time_slot-1] / (Cluster.dt * 60) * Timeframe.windowsize.seconds
        # 对区域顾客到达速率进行放大
        V_arrival = V_arrival * amplification_factor
        # 该区域单位时间生成num_of_arrivals个顾客的概率
        P_produce = exp(-V_arrival)*pow(V_arrival, num_of_arrivals) / factorial(num_of_arrivals)
        # 判断是否生成num_of_arrivals个顾客
        P_temp = random.random()
        if P_temp < P_produce:
            # 生成num_of_arrivals个顾客
            for i in range(num_of_arrivals):
                pickup_id = random.sample(cluster.grids_included, 1) + num_of_intersections
                temp = random.randint(1,delivery_hot_index[time_slot-1][num_of_durations])
                for j in range(len(delivery_clusters)):
                    if temp > delivery_hot_index[time_slot-1][j] and temp <= delivery_hot_index[time_slot-1][j+1]:
                        delivery_id = random.sample(delivery_clusters[j+1-1].grids_included, 1) + num_of_intersections
                        cluster.query_list.append(Query(query_id, pickup_id, delivery_id, starttime))
                        query_id += 1
                        break

    ## 判断每个区域此刻的订单数是否超过阈值
    for cluster in pickup_clusters:
        if len(cluster.query_list) > RON_threshold:
            # 拼单算法（包括寻找空车司机以及路径规划）
            pass
        else:
            # 双边查找算法
            pass
            # 插入检测
            pass

    ## 空车司机使用推荐算法

    ## 更新司机当前位置，以及更新每个格子区域司机列表
    for driver in driver_list:
        # 如果司机车上乘客不为0
        if driver.num_of_occupied_position > 0 and driver.num_of_occupied_position*2 != len(driver.cur_schedule):
            driver.total_time_traveled += (endtime-starttime).seconds
        # 司机行驶到下一个点
        driver.reach_the_next_point((endtime-starttime).seconds)
        # 跟踪司机0的轨迹
        if driver.driver_id == 0:
            print("-------------------------------------------")
            print(starttime)
            print(driver.cur_location)
            print(driver.cur_schedule)
            print(driver.route)
            print(driver.assist_t)
            print(driver.num_of_occupied_position)
            print(driver.total_time_traveled)

    ## 删除被服务的订单
    for cluster in pickup_clusters:
        cluster.query_list = [query for query in cluster.query_list if query.condition == 0]

    ## 删除过期订单
    for cluster in pickup_clusters:
        cluster.query_list = [query for query in cluster.query_list if endtime > query.latest_pickup_time]

    ## 删除每个格子里的driver_will_coming列表中endtime之前的所有记录
    for grid in regl_Hexg_grids:
        while True:
            if grid.driver_will_coming[0][1] <= endtime:
                del grid.driver_will_coming[0]
            else:
                break

    ## 下一次循环
    starttime = endtime
    endtime = endtime + Timeframe.windowsize

## 算法结束时，有的车还没有跑完route中的所有点，在这里接着跑完

## 打印输出信息