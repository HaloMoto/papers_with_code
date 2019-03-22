#! /usr/bin/env python
# -*- coding: utf-8 -*-

from preparation_work.cal_distance import cal_distance
from bean.SGrid import SGrid
from math import ceil
from dao.dbconnect import *
from preparation_work.Constant import LL

# 对地图进行正方形格子全覆盖
sqr_grids = []
# 格子边长
side_length = 100

# 求正方形格子的中心点
# 中间变量
temp = ceil(2100/side_length)
for i in range(temp):
    for j in range(temp):
        sqr_grids.append(SGrid(temp*i+j+1, side_length*i+side_length/2, side_length*j+side_length/2))

### 统计每个格子的历史接载点数据 ###
# 连接数据库
connection_object = ()
# 获得游标
cursor = connection_object.cursor()
# 查询语句并执行
q = "select Pickup_longitude, Pickup_latitude from trip where Pickup_longitude <= -73.906124 and Pickup_longitude >= -73.929870 and Pickup_latitude >= 40.645793 and Pickup_latitude <= 40.663759"
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
q = "select Dropoff_longitude,Dropoff_latitude from trip where Dropoff_longitude <= -73.906124 and Dropoff_longitude >= -73.929870 and Dropoff_latitude >= 40.645793 and Dropoff_latitude <= 40.663759"
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
