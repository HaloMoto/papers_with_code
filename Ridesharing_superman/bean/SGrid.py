#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import fabs

class SGrid:
    def __init__(self, grid_id, center_x, center_y, side_length):
        # 正方形格子标号
        self.grid_id = grid_id
        # 正方形格子中心点x轴坐标
        self.center_x = center_x
        # 正方形格子中心点y轴坐标
        self.center_y = center_y
        # 正方形格子中心点的经纬度
        self.center = None
        # 正方形格子的锚点
        self.anchor = None
        # 正方形格子边长
        self.side_length = side_length
        # 当前在格子内的司机以及未来将进入格子内的司机列表
        self.driver_will_coming = []
        # 格子属于哪个接载点区域
        self.pickup_cluster = []
        # 格子属于哪个传送点区域
        self.delivery_cluster = []
        # 该区域接载点历史数据
        self.pickup_history = []
        # 该区域传送点历史数据
        self.delivery_history = []
        # 格子内十字路口集合
        self.cross_points = []
        # 锚点相邻的十字路口
        self.nearest = []

    # 类打印函数
    def __str__(self):
        return 'grid id: %d, center (%f,%f)'%(self.grid_id, self.center_x, self.center_y)

    # 这个类能够判断点是否在正方形格子内
    def is_in_this_grid(self, point):
        if fabs(point[0]-self.center_x) <= self.side_length/2 and fabs(point[1]-self.center_y) <= self.side_length/2:
            return True
        else:
            return False

    # 增加一个接载点历史节点
    def add_pickup_history_point(self, point):
        self.pickup_history.append([point[0], point[1], self.grid_id, point[2]])

    # 增加一个传送点历史节点
    def add_delivery_history_point(self, point):
        self.delivery_history.append([point[0], point[1], self.grid_id, point[2]])