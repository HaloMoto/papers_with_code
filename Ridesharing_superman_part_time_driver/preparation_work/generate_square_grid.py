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
    first_nearest = nodes[0]
    second_nearest = nodes[0]
    first_distance = cal_distance(lon1=grid.anchor[0], lat1=grid.anchor[1], lon2=nodes[0][0], lat2=nodes[0][1]).twopoint_distance()
    second_distance = first_distance
    for node in nodes:
        distance = cal_distance(lon1=grid.anchor[0], lat1=grid.anchor[1], lon2=node[0], lat2=node[1]).twopoint_distance()
        if distance > second_distance:
            if distance > first_distance:
                second_nearest = first_nearest
                second_distance = first_distance
                first_nearest = node
                first_distance = distance
            else:
                second_nearest = node
                second_distance = distance
    grid.nearest.append(first_nearest)
    grid.nearest.append(second_nearest)

### 生成接载点cluster ###
# cluster数目
num_of_pickup_cluster = 20
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

### 每个区域每天每个固定长的时间段的订单数分布 ###
# 时间段长度,单位为分钟
dt = 5
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

### 计算每个区域每个时间段的均值和方差 ###
for cluster in pickup_clusters:
    cluster.avg_of_each_duration = np.mean(np.array(cluster.records), axis=0)
    cluster.var_of_each_duration = np.var(np.array(cluster.records), axis=0)
    print(cluster.avg_of_each_duration)
    print(cluster.var_of_each_duration)