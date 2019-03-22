#!/usr/bin/python
# -*- coding: utf-8 -*-

class Cluster:
    def __init__(self, cluster_id):
        # 区域的标号
        self.cluster_id = cluster_id
        # 区域包含哪些格子
        self.grids_included = {}
        # 区域的锚点
        self.anchor = None
        # 区域过去12天，每天每个时间段的统计数
        self.records = []

