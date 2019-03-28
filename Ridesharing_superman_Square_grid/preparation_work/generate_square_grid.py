#! /usr/bin/env python
# -*- coding: utf-8 -*-

from preparation_work.cal_distance import cal_distance
from math import ceil,floor,sqrt
from bean.SGrid import SGrid
from dao.dbconnect import *
from preparation_work.Constant import LL
from scipy.cluster.vq import kmeans2
import numpy as np
from service.Auxiliary import coord2lonlat
from bean.Cluster import Cluster
from config.Timeframe import *
import pickle
from bean.Driver import Driver
import sys

# 对地图进行正方形格子全覆盖
sqr_grids = []
# 格子边长
side_length = 100

# 求正方形格子的中心点
# 中间变量
temp = ceil(2100/side_length)
for i in range(temp):
    for j in range(temp):
        sqr_grids.append(SGrid(temp*i+j+1, side_length*i+side_length/2, side_length*j+side_length/2, side_length))

### 计算各格子中心点的经纬度 ###
for grid in sqr_grids:
    grid.center = coord2lonlat((grid.center_x, grid.center_y), LL)
    point = [grid.center[0], grid.center[1], datetime.datetime(2014, 2, 1, 0, 30, 0)]
    grid.add_pickup_history_point(point)
    grid.add_delivery_history_point(point)

### 统计每个格子的历史接载点数据 ###
# 连接数据库
connection_object = open_db_connection1()
# 获得游标
cursor = connection_object.cursor()
# 查询语句并执行
q = "select Pickup_longitude, Pickup_latitude, Lpep_pickup_datetime from trip where Pickup_longitude <= -73.906124 and Pickup_longitude >= -73.929870 and Pickup_latitude >= 40.645793 and Pickup_latitude <= 40.663759"
cursor.execute(q)
# # 获取第一条数据
# first_record = cursor.fetchone()
# 遍历查询结果
if cursor != None:
    for point in cursor:
        distance1 = cal_distance(lat1=point[1], lon1=point[0], lat2=point[1], lon2=LL[0])
        distance2 = cal_distance(lat1=point[1], lon1=point[0], lat2=LL[1], lon2=point[0])
        # point在地图上的坐标点
        point_temp = (distance1.twopoint_distance(), distance2.twopoint_distance())
        # 判断点属于哪个格子
        for grid in sqr_grids:
            if grid.is_in_this_grid(point_temp):
                grid.add_pickup_history_point(point)
                break
# 关闭数据库连接
close_db_connection(connection_object)
### 统计每个格子的历史传送点数据 ###
# 连接数据库
connection_object = open_db_connection1()
# 获取游标
cursor = connection_object.cursor()
# 编辑获取传送点数据的查询语句并执行
q = "select Dropoff_longitude,Dropoff_latitude,Lpep_dropoff_datetime from trip where Dropoff_longitude <= -73.906124 and Dropoff_longitude >= -73.929870 and Dropoff_latitude >= 40.645793 and Dropoff_latitude <= 40.663759"
cursor.execute(q)
# 遍历查询结果
if cursor != None:
    for point in cursor:
        distance1 = cal_distance(lat1=point[1], lon1=point[0], lat2=point[1], lon2=LL[0])
        distance2 = cal_distance(lat1=point[1], lon1=point[0], lat2=LL[1], lon2=point[0])
        # 计算point在地图中的坐标
        point_temp = (distance1.twopoint_distance(), distance2.twopoint_distance())
        for grid in sqr_grids:
            if grid.is_in_this_grid(point_temp):
                grid.add_delivery_history_point(point)
                break
# 关闭数据库连接
close_db_connection(connection_object)
### 统计每个格子的历史传送点数据 ###
# 连接数据库
connection_object = open_db_connection1()
# 获取游标
cursor = connection_object.cursor()
# 编辑获取传送点数据的查询语句并执行
q = "select Dropoff_longitude,Dropoff_latitude, Lpep_dropoff_datetime from trip where Dropoff_longitude <= -73.906124 and Dropoff_longitude >= -73.929870 and Dropoff_latitude >= 40.645793 and Dropoff_latitude <= 40.663759"
cursor.execute(q)
# 遍历查询结果
if cursor != None:
    for point in cursor:
        distance1 = cal_distance(lat1=point[1], lon1=point[0], lat2=point[1], lon2=LL[0])
        distance2 = cal_distance(lat1=point[1], lon1=point[0], lat2=LL[1], lon2=point[0])
        # 计算point在地图中的坐标
        point_temp = (distance1.twopoint_distance(), distance2.twopoint_distance())
        for grid in sqr_grids:
            if grid.is_in_this_grid(point_temp):
                grid.add_delivery_history_point(point)
                break

### 用kmeans算法计算每个格子的锚点 ###
# 循环遍历每个格子
for grid in sqr_grids:
    # 将pickup历史数据转换为np.array
    # print(grid.pickup_history)
    coordinates = np.array(grid.pickup_history)[:,0:2]
    coordinates = coordinates.astype(np.float64)
    print(coordinates)
    # 调用kmeans2算法，进行聚类，这一步的主要目的是求出每个格子的锚点
    centroid,label = kmeans2(coordinates, 1, iter=20, minit='points')
    grid.anchor = centroid[0]

### 从文件中读取十字路口数据入nodes数组 ###
nodes = []
# 读的方式打开node.txt文件
with open("../data/node.txt", "r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        longitude, latitude, node_id = lines.split(",")
        longitude = float(longitude)
        latitude = float(latitude)
        node_id = int(node_id)
        nodes.append((longitude, latitude))

### 寻找距离每个锚点最近的两个十字路口 ###
for grid in sqr_grids:
    first_nearest = 0
    second_nearest = 0
    first_distance = cal_distance(lon1=grid.anchor[0], lat1=grid.anchor[1], lon2=nodes[0][0], lat2=nodes[0][1]).twopoint_distance()
    second_distance = first_distance
    for i in range(len(nodes)):
        distance = cal_distance(lon1=grid.anchor[0], lat1=grid.anchor[1], lon2=nodes[i][0], lat2=nodes[i][1]).twopoint_distance()
        if distance < second_distance:
            if distance < first_distance:
                second_nearest = first_nearest
                second_distance = first_distance
                first_nearest = i
                first_distance = distance
            else:
                second_nearest = i
                second_distance = distance
    grid.nearest.append(first_nearest+1)
    grid.nearest.append(second_nearest+1)

### 生成接载点cluster ###
# cluster数目
num_of_pickup_cluster = 10
# cluster集合
pickup_clusters = []
# 每个区域的历史接载点集合
pickup_history = []
for grid in sqr_grids:
    pickup_history.extend(grid.pickup_history)
# 对接载点进行kmeans聚类
centroid, labels = kmeans2(np.array(pickup_history)[:, 0:2].astype(np.float64), num_of_pickup_cluster, iter=20, minit='points')
# 接载区域锚点
for i in range(len(centroid)):
    pickup_clusters.append(Cluster(i+1))
    pickup_clusters[i].anchor = centroid[i]
# 保存区域包含的格子，以及格子所属的区域
for i in range(len(labels)):
    pickup_clusters[labels[i]].grids_included.add(pickup_history[i][2])
    sqr_grids[pickup_history[i][2]-1].pickup_cluster.append(labels[i]+1)
# 去重处理
for grid in sqr_grids:
    grid.pickup_cluster = list(set(grid.pickup_cluster))

### 生成传送点cluster ###
# cluster数目
num_of_delivery_cluster = 10
# cluster集合
delivery_clusters = []
# 每个区域的历史接载点集合
delivery_history = []
for grid in sqr_grids:
    delivery_history.extend(grid.delivery_history)
# 对接载点进行kmeans聚类
centroid, labels = kmeans2(np.array(delivery_history)[:, 0:2].astype(np.float64), num_of_pickup_cluster, iter=20, minit='points')
for i in range(len(centroid)):
    delivery_clusters.append(Cluster(i+1))
    delivery_clusters[i].anchor = centroid[i]
for i in range(len(labels)):
    delivery_clusters[labels[i]].grids_included.add(delivery_history[i][2])
    sqr_grids[delivery_history[i][2]-1].delivery_cluster.append(labels[i]+1)
# 去重处理
for grid in sqr_grids:
    grid.delivery_cluster = list(set(grid.delivery_cluster))

### 每个区域每天每个固定长的时间段的订单数分布 ###
# 时间段长度,单位为分钟
dt = Cluster.dt
# 模拟开始时间
starttime1 = starttime
# 模拟结束时间
endtime1 = untildatetime
# 时间段数目
num_of_duration = (endtime1-starttime1).seconds / 60 / dt
# 对时间段进行放大
dt_enlarge = 24/num_of_duration
# 统计每个区域每个时间段的订单数
for cluster in pickup_clusters:
    # 每个区域保存时间段长度
    cluster.dt = dt
    # 每个区域保存时间段数目
    cluster.num_of_duration = num_of_duration
    ## 保存该区域一月份的历史纪录 ##
    statistic_1 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-01-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-01-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_1
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_1.append(point)
    # 统计该区域在一月份不同时段的记录数
    record_1 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_1列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_1:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_1
        record_1.append(sum)
    cluster.records.append(record_1)

    ## 保存该区域二月份的历史纪录 ##
    statistic_2 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-02-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-02-28', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_2
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_2.append(point)
    # 统计该区域在二月份不同时段的记录数
    record_2 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_2列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_2:
            # print(point[3].time())
            # print(d_time)
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_2
        record_2.append(sum)
    cluster.records.append(record_2)

    ## 保存该区域三月份的历史纪录 ##
    statistic_3 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-03-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-03-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_3
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_3.append(point)
    # 统计该区域在三月份不同时段的记录数
    record_3 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_1列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_3:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_3
        record_3.append(sum)
    cluster.records.append(record_3)

    ## 保存该区域四月份的历史纪录 ##
    statistic_4 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-04-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-04-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_1
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_4.append(point)
    # 统计该区域在四月份不同时段的记录数
    record_4 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_4列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_4:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_4
        record_4.append(sum)
    cluster.records.append(record_4)

    ## 保存该区域五月份的历史纪录 ##
    statistic_5 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-05-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-05-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_5
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_5.append(point)
    # 统计该区域在五月份不同时段的记录数
    record_5 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_5列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_5:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_5
        record_5.append(sum)
    cluster.records.append(record_5)

    ## 保存该区域六月份的历史纪录 ##
    statistic_6 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-06-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-06-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_6
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_6.append(point)
    # 统计该区域在六月份不同时段的记录数
    record_6 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_6列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_6:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_6
        record_6.append(sum)
    cluster.records.append(record_6)

    ## 保存该区域七月份的历史纪录 ##
    statistic_7 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-07-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-07-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_7
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_7.append(point)
    # 统计该区域在七月份不同时段的记录数
    record_7 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_7列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_7:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_7
        record_7.append(sum)
    cluster.records.append(record_7)

    ## 保存该区域八月份的历史纪录 ##
    statistic_8 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-08-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-08-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_8
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_8.append(point)
    # 统计该区域在八月份不同时段的记录数
    record_8 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_8列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_8:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_8
        record_8.append(sum)
    cluster.records.append(record_8)

    ## 保存该区域九月份的历史纪录 ##
    statistic_9 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-09-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-09-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_9
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_9.append(point)
    # 统计该区域在九月份不同时段的记录数
    record_9 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_9列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_9:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_9
        record_9.append(sum)
    cluster.records.append(record_9)

    ## 保存该区域十月份的历史纪录 ##
    statistic_10 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-10-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-10-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_10
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_10.append(point)
    # 统计该区域在十月份不同时段的记录数
    record_10 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_10列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_10:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_10
        record_10.append(sum)
    cluster.records.append(record_10)

    ## 保存该区域十一月份的历史纪录 ##
    statistic_11 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-11-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-11-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_11
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_11.append(point)
    # 统计该区域在十一月份不同时段的记录数
    record_11 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_11列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_11:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_11
        record_11.append(sum)
    cluster.records.append(record_11)

    ## 保存该区域十二月份的历史纪录 ##
    statistic_12 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-12-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-12-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_12
        for point in sqr_grids[grid_id-1].pickup_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_12.append(point)
    # 统计该区域在十二月份不同时段的记录数
    record_12 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_12列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_12:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_12
        record_12.append(sum)
    cluster.records.append(record_12)

# 统计每个区域（delivery_clusters）每个时间段里传送点的订单数
for cluster in delivery_clusters:
    # 每个区域保存时间段长度
    cluster.dt = dt
    # 每个区域保存时间段数目
    cluster.num_of_duration = num_of_duration
    ## 保存该区域一月份的历史纪录 ##
    statistic_1 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-01-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-01-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_1
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_1.append(point)
    # 统计该区域在一月份不同时段的记录数
    record_1 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_1列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_1:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_1
        record_1.append(sum)
    cluster.records.append(record_1)

    ## 保存该区域二月份的历史纪录 ##
    statistic_2 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-02-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-02-28', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_2
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_2.append(point)
    # 统计该区域在二月份不同时段的记录数
    record_2 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_2列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_2:
            # print(point[3].time())
            # print(d_time)
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_2
        record_2.append(sum)
    cluster.records.append(record_2)

    ## 保存该区域三月份的历史纪录 ##
    statistic_3 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-03-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-03-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_3
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_3.append(point)
    # 统计该区域在三月份不同时段的记录数
    record_3 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_1列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_3:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_3
        record_3.append(sum)
    cluster.records.append(record_3)

    ## 保存该区域四月份的历史纪录 ##
    statistic_4 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-04-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-04-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_1
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_4.append(point)
    # 统计该区域在四月份不同时段的记录数
    record_4 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_4列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_4:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_4
        record_4.append(sum)
    cluster.records.append(record_4)

    ## 保存该区域五月份的历史纪录 ##
    statistic_5 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-05-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-05-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_5
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_5.append(point)
    # 统计该区域在五月份不同时段的记录数
    record_5 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_5列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_5:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_5
        record_5.append(sum)
    cluster.records.append(record_5)

    ## 保存该区域六月份的历史纪录 ##
    statistic_6 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-06-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-06-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_6
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_6.append(point)
    # 统计该区域在六月份不同时段的记录数
    record_6 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_6列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_6:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_6
        record_6.append(sum)
    cluster.records.append(record_6)

    ## 保存该区域七月份的历史纪录 ##
    statistic_7 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-07-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-07-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_7
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_7.append(point)
    # 统计该区域在七月份不同时段的记录数
    record_7 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_7列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_7:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_7
        record_7.append(sum)
    cluster.records.append(record_7)

    ## 保存该区域八月份的历史纪录 ##
    statistic_8 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-08-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-08-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_8
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_8.append(point)
    # 统计该区域在八月份不同时段的记录数
    record_8 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_8列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_8:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_8
        record_8.append(sum)
    cluster.records.append(record_8)

    ## 保存该区域九月份的历史纪录 ##
    statistic_9 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-09-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-09-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_9
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_9.append(point)
    # 统计该区域在九月份不同时段的记录数
    record_9 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_9列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_9:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_9
        record_9.append(sum)
    cluster.records.append(record_9)

    ## 保存该区域十月份的历史纪录 ##
    statistic_10 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-10-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-10-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_10
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_10.append(point)
    # 统计该区域在十月份不同时段的记录数
    record_10 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_10列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_10:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_10
        record_10.append(sum)
    cluster.records.append(record_10)

    ## 保存该区域十一月份的历史纪录 ##
    statistic_11 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-11-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-11-30', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_11
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_11.append(point)
    # 统计该区域在十一月份不同时段的记录数
    record_11 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_11列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_11:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_11
        record_11.append(sum)
    cluster.records.append(record_11)

    ## 保存该区域十二月份的历史纪录 ##
    statistic_12 = []
    # 范围时间
    d_time = datetime.datetime.strptime('2014-12-01', '%Y-%m-%d')
    d_time1 = datetime.datetime.strptime('2014-12-31', '%Y-%m-%d')
    # 遍历区域内所有的格子
    for grid_id in cluster.grids_included:
        # 遍历格子内所有记录,并将在约束条件内的点加入statistic_12
        for point in sqr_grids[grid_id-1].delivery_history:
            if point[3] >= d_time and point[3] <= d_time1:
                statistic_12.append(point)
    # 统计该区域在十二月份不同时段的记录数
    record_12 = []
    for i in range(int(num_of_duration)):
        # 范围时间
        d_time = datetime.datetime.strptime('%d:00:00'%(dt_enlarge*i), '%H:%M:%S').time()
        d_time1 = datetime.datetime.strptime('%d:59:59'%(dt_enlarge*(i+1)-1), '%H:%M:%S').time()
        # 遍历statistic_12列表
        sum = 0
        # 统计特定时间段的数据
        for point in statistic_12:
            if point[3].time() >= d_time and point[3].time() <= d_time1:
                sum += 1
        # 将统计结果保存入record_12
        record_12.append(sum)
    cluster.records.append(record_12)

### 计算每个区域每个时间段的均值和方差 ###
for cluster in pickup_clusters:
    cluster.avg_of_each_duration = np.mean(np.array(cluster.records), axis=0)
    cluster.var_of_each_duration = np.var(np.array(cluster.records), axis=0)
    print(cluster.avg_of_each_duration)
    print(cluster.var_of_each_duration)

### 计算每个传送点区域每个时间段的均值和方差 ###
for cluster in delivery_clusters:
    cluster.avg_of_each_duration = np.mean(np.array(cluster.records), axis=0)
    cluster.var_of_each_duration = np.var(np.array(cluster.records), axis=0)

### 计算距离区域锚点最近的两个十字路口 ###
for cluster in pickup_clusters:
    first_nearest = 0
    second_nearest = 0
    first_distance = cal_distance(lon1=cluster.anchor[0], lat1=cluster.anchor[1], lon2=nodes[0][0], lat2=nodes[0][1]).twopoint_distance()
    second_distance = first_distance
    for i in range(len(nodes)):
        distance = cal_distance(lon1=cluster.anchor[0], lat1=cluster.anchor[1], lon2=nodes[i][0], lat2=nodes[i][1]).twopoint_distance()
        if distance < second_distance:
            if distance < first_distance:
                second_nearest = first_nearest
                second_distance = first_distance
                first_nearest = i
                first_distance = distance
            else:
                second_nearest = i
                second_distance = distance
    cluster.nearest.append(first_nearest+1)
    cluster.nearest.append(second_nearest+1)

### 保存所有节点 ###
# 十字路口数
num_of_intersections = len(nodes)
# 格子数
num_of_grids = len(sqr_grids)
# 区域数
num_of_clusters = len(pickup_clusters)
print(num_of_intersections, num_of_grids, num_of_clusters)
# 写的方式打开node_all.txt
f = open("../data/node_all.txt", "w")
# 先写入十字路口数， 再写入格子锚点数， 再写入区域锚点数
f.write(str(num_of_intersections)+'\n')
f.write(str(num_of_grids)+'\n')
f.write(str(num_of_clusters)+'\n')
# 写入所有十字路口坐标
for i in range(1, num_of_intersections+1):
    f.write(str(nodes[i-1][0]) + ' ' + str(nodes[i-1][1]) + ' ' + str(i) + '\n')
# 写入所有格子锚点坐标
for i in range(num_of_grids):
    f.write(str(sqr_grids[i].anchor[0]) + ' ' + str(sqr_grids[i].anchor[1]) + ' ' + str(num_of_intersections+i+1) + '\n')
# 写入所有区域锚点坐标
for i in range(num_of_clusters):
    f.write(str(pickup_clusters[i].anchor[0]) + ' ' + str(pickup_clusters[i].anchor[1]) + ' ' + str(num_of_intersections+num_of_grids+i+1) + '\n')
f.close()

### 保存所有的边 ###
# 总边数
num_of_edges = 0
# 写的方式打开edge.txt文件
f = open("../data/edge_all.txt","w")
# 读取edge.txt文件里的内容，并保存入edge_all.txt文件
with open("../data/edge.txt", "r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        start, end = [int(i) for i in lines.split(",")]
        f.write(str(start) + ' ' + str(end) + '\n')
        num_of_edges += 1
# 写入距离格子锚点最近两个点的边
for i in range(len(sqr_grids)):
    f.write(str(num_of_intersections+i+1) + ' ' + str(sqr_grids[i].nearest[0]) + '\n')
    f.write(str(sqr_grids[i].nearest[0]) + ' ' + str(num_of_intersections + i + 1) + '\n')
    f.write(str(num_of_intersections+i+1) + ' ' + str(sqr_grids[i].nearest[1]) + '\n')
    f.write(str(sqr_grids[i].nearest[1]) + ' ' + str(num_of_intersections + i + 1) + '\n')
    num_of_edges += 4
# 写入距离区域锚点最近两个点的边
for i in range(len(pickup_clusters)):
    f.write(str(num_of_intersections+num_of_grids+i+1) + ' ' + str(pickup_clusters[i].nearest[0]) + '\n')
    f.write(str(pickup_clusters[i].nearest[0]) + ' ' + str(num_of_intersections+num_of_grids+i+1) + '\n')
    f.write(str(num_of_intersections+num_of_grids+i+1) + ' ' + str(pickup_clusters[i].nearest[1]) + '\n')
    f.write(str(pickup_clusters[i].nearest[1]) + ' ' + str(num_of_intersections+num_of_grids+i+1) + '\n')
    num_of_edges += 4
f.close()

### 计算所有的边长 ###
# 读取node_all.txt文件里的所有内容
nodes_all = []
with open("../data/node_all.txt","r") as file_to_read:
    # 从文件中读取十字路口数
    num_of_intersections = int(file_to_read.readline())
    # 从文件中读取格子数
    num_of_grids = int(file_to_read.readline())
    # 从文件中读取聚类数
    num_of_clusters = int(file_to_read.readline())
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        longitude, latitude, node_id = lines.split()
        longitude = float(longitude)
        latitude = float(latitude)
        node_id = int(node_id)
        nodes_all.append((longitude, latitude))
# 保存所有边的长度进入文件edge_all_length.txt
f = open("../data/edge_all_length.txt","w")
f.write(str(num_of_intersections+num_of_grids+num_of_clusters) + '\n')
f.write(str(num_of_edges) + '\n')
with open("../data/edge_all.txt","r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        start, end = [int(i) for i in lines.split()]
        distance_temp = cal_distance(lat1=nodes_all[start-1][1], lon1=nodes_all[start-1][0], lat2=nodes_all[end-1][1], lon2=nodes_all[end-1][0])
        f.write(str(start) + ' ' + str(end) + ' ' + str(int(distance_temp.twopoint_distance())) + '\n')
    f.close()

### 计算每条边经过所需要的时间 ###
### 保存所有点之间的最短路径 ###
### 将所有点到某个点的空间距离从近到远排列 ###
### 将所有点到某个点的时间距离从近到远排列 ###
# 打开文件edge_all_length.txt
try:
    fil= open("../data/edge_all_length.txt","r")
except IOError:
    print("File not found.")
    sys.exit(-1)
# 点数
V = int(fil.readline().strip())
# 最短路径空间距离数组
dist = []
# 最短路径时间距离数组
time = []
# 最短路径数组
parent = []
# 边数
E = int(fil.readline().strip())
# 初始化无限距离
for i in range(0, V):
    dist.append([])
    parent.append([])
    time.append([])
    for j in range(0, V):
        dist[i].append(float("inf"))
        time[i].append(float("inf"))
        parent[i].append(0)
# 从文件中读取边信息
for i in range(0, E):
    t = fil.readline().strip().split()
    x = int(t[0]) - 1
    y = int(t[1]) - 1
    w = int(t[2])
    dist[x][y] = w
    parent[x][y] = x
# 自反点的距离设为0
for i in range(0, V):
    dist[i][i] = 0
# 初始化路径数组
for i in range(0,V):
    for j in range(0,V):
        if dist[i][j] == float("inf"):
            parent[i][j] = 0
        else:
            parent[i][j] = i
# Floyd warshall算法
for k in range(0,V):
    for i in range(0,V):
        for j in range(0,V):
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                parent[i][j] = parent[k][j]
# 计算旅行时间
for i in range(V):
    for j in range(V):
        time[i][j] = dist[i][j] / Driver.speed
# 保存输出
np.savetxt("../data/dist.txt", dist, fmt='%-3.0f')
np.savetxt("../data/route.txt", parent, fmt='%-3d')
np.savetxt("../data/time.txt", time, fmt='%-3.0f')
fil.close()

### 基于所有格子的紧密性给出节点的顺序 ###
# 使用Floyd算法得到的dist.txt和time.txt矩阵
D = np.loadtxt('../data/dist.txt')
T = np.loadtxt('../data/time.txt')
# 截取格子锚点之间的时空距离矩阵
D = D[num_of_intersections:num_of_intersections+num_of_grids, num_of_intersections:num_of_intersections+num_of_grids]
T = T[num_of_intersections:num_of_intersections+num_of_grids, num_of_intersections:num_of_intersections+num_of_grids]
Gd = np.zeros([num_of_grids, num_of_grids])
Gt = np.zeros([num_of_grids, num_of_grids])
for i in range(1, num_of_grids+1):
    Gd[i-1] = np.argsort(D[i-1], kind='quicksort', order=None)+1
    Gt[i-1] = np.argsort(T[i-1], kind='quicksort', order=None)+1
# 保存输出
np.savetxt('../data/Gd.txt', Gd, fmt='%-3.0f')
np.savetxt('../data/Gt.txt', Gt, fmt='%-3.0f')

### 基于所有区域的紧密性给出节点的顺序 ###
# 使用Floyd算法得到的dist.txt和time.txt矩阵
D = np.loadtxt('../data/dist.txt')
T = np.loadtxt('../data/time.txt')
# 截取格子锚点之间的时空距离矩阵
D = D[num_of_intersections+num_of_grids:num_of_intersections+num_of_grids+num_of_clusters, num_of_intersections+num_of_grids:num_of_intersections+num_of_grids+num_of_clusters]
T = T[num_of_intersections+num_of_grids:num_of_intersections+num_of_grids+num_of_clusters, num_of_intersections+num_of_grids:num_of_intersections+num_of_grids+num_of_clusters]
Gd = np.zeros([num_of_clusters, num_of_clusters])
Gt = np.zeros([num_of_clusters, num_of_clusters])
for i in range(1, num_of_clusters+1):
    Gd[i-1] = np.argsort(D[i-1], kind='quicksort', order=None)+1
    Gt[i-1] = np.argsort(T[i-1], kind='quicksort', order=None)+1
# 保存输出
np.savetxt('../data/Gd_c.txt', Gd, fmt='%-3.0f')
np.savetxt('../data/Gt_c.txt', Gt, fmt='%-3.0f')

### 保存格子数组 ###
with open('../data/sqr_grids.txt', 'wb') as f:
    pickle.dump(sqr_grids, f)

### 保存区域数组 ###
with open('../data/pickup_clusters.txt', 'wb') as f:
    pickle.dump(pickup_clusters, f)
with open('../data/delivery_clusters.txt', 'wb') as f:
    pickle.dump(delivery_clusters, f)

### 十字路口所属格子 ###
nodes_belong_to_which_grid = dict()
# 计算格子包含哪些十字路口
for i in range(len(nodes)):
    distance1 = cal_distance(lat1=nodes[i][1], lon1=nodes[i][0], lat2=nodes[i][1], lon2=LL[0])
    distance2 = cal_distance(lat1=nodes[i][1], lon1=nodes[i][0], lat2=LL[1], lon2=nodes[i][0])
    # 计算point在地图中的坐标
    point_temp = (distance1.twopoint_distance(), distance2.twopoint_distance())
    for grid in sqr_grids:
        if grid.is_in_this_grid(point_temp):
            grid.cross_points.append(i+1)
            break
# 格子锚点所属格子
for i in range(len(sqr_grids)):
    distance1 = cal_distance(lat1=sqr_grids[i].anchor[1], lon1=sqr_grids[i].anchor[0], lat2=sqr_grids[i].anchor[1], lon2=LL[0])
    distance2 = cal_distance(lat1=sqr_grids[i].anchor[1], lon1=sqr_grids[i].anchor[0], lat2=LL[1], lon2=sqr_grids[i].anchor[0])
    # 计算point在地图中的坐标
    point_temp = (distance1.twopoint_distance(), distance2.twopoint_distance())
    for grid in sqr_grids:
        if grid.is_in_this_grid(point_temp):
            grid.cross_points.append(num_of_intersections + i + 1)
            break
# 区域锚点所属格子
for i in range(len(pickup_clusters)):
    distance1 = cal_distance(lat1=pickup_clusters[i].anchor[1], lon1=pickup_clusters[i].anchor[0], lat2=pickup_clusters[i].anchor[1], lon2=LL[0])
    distance2 = cal_distance(lat1=pickup_clusters[i].anchor[1], lon1=pickup_clusters[i].anchor[0], lat2=LL[1], lon2=pickup_clusters[i].anchor[0])
    # 计算point在地图中的坐标
    point_temp = (distance1.twopoint_distance(), distance2.twopoint_distance())
    for grid in sqr_grids:
        if grid.is_in_this_grid(point_temp):
            grid.cross_points.append(num_of_intersections + num_of_grids + i + 1)
            break
# 计算十字路口所属格子字典
for i in range(len(sqr_grids)):
    for j in sqr_grids[i].cross_points:
        nodes_belong_to_which_grid[j] = i+1
# 保存该字典
with open('../data/nodes_belong_to_which_grid.txt', 'wb') as f:
    pickle.dump(nodes_belong_to_which_grid, f)

### 位置查询 ###
np.savetxt("../data/location_query.txt",nodes_all)
# LQ = np.loadtxt('../data/location_query.txt')
# print(LQ[0][0], LQ[0][1])