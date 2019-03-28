#!/usr/bin/python
# -*- coding: utf-8 -*-

class Cluster:
    dt = 5
    def __init__(self, cluster_id):
        # 区域的标号
        self.cluster_id = cluster_id
        # 区域包含哪些格子
        self.grids_included = set()
        # 时间段长度
        self.dt = None
        # 时间段数目
        self.num_of_duration = None
        # 各个时间段的平均值
        self.avg_of_each_duration = []
        # 各个时间段的方差
        self.var_of_each_duration = []
        # 区域的锚点
        self.anchor = None
        # 区域过去12天，每天每个时间段的统计数
        self.records = []
        # 锚点相邻的十字路口
        self.nearest = []
        # 订单列表
        self.query_list = []

