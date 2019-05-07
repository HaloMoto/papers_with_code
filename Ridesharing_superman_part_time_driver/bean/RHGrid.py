#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import fabs,sqrt

class RHGrid:
    def __init__(self, grid_id, center_x, center_y, side_length):
        # 正六边形格子的标号
        self.grid_id = grid_id
        # 正六边形格子中点的x轴
        self.center_x = center_x
        # 正六边形格子中点的y轴
        self.center_y = center_y
        # 正六边形格子中点的经纬度
        self.center = None
        # 正六边形格子的锚点
        self.anchor = None
        # 格子边长
        self.side_length = side_length
        # 已在格子里的司机和未来时间将进入格子的司机列表，按照时间先后循序排列
        self.driver_will_coming = []
        # 格子属于哪个接载点区域
        self.pickup_cluster = []
        # 格子属于哪个传送点区域
        self.delivery_cluster = []
        # 该区域接载点历史数据
        self.pickup_history = []
        # 该区域传送点历史数据
        self.delivery_history = []
        # 格子内的十字路口集合
        self.cross_points = []
        # 锚点相邻的十字路口
        self.nearest = []

    # 类的打印方法
    def __str__(self):
        return 'grid id: %d, center (%f, %f)'%(self.grid_id, self.center_x, self.center_y)

    # 判断一个点是否在格子内
    def is_in_this_grid(self, point):
        if fabs(point[0] - self.center_x) >= self.side_length or fabs(point[1] - self.center_y) >= self.side_length*sqrt(3)/2:
            return False
        elif self.side_length - fabs(point[0] - self.center_x) > fabs(point[1]-self.center_y)*sqrt(3)/3:
            return True

    # 增加一个接载点历史节点
    def add_pickup_history_point(self, point):
        self.pickup_history.append([point[0], point[1], self.grid_id, point[2]])

    # 增加一个传送点历史节点
    def add_delivery_history_point(self, point):
        self.delivery_history.append([point[0], point[1], self.grid_id, point[2]])
