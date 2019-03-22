#! /usr/bin/env python
# -*- coding: utf-8 -*-

from math import fabs,sqrt

class Partition:
    def __init__(self, partition_id, center_x, center_y):
        self.partition_id = partition_id
        self.center_x = center_x
        self.center_y = center_y
        self.anchor = None
        self.hot_index = 0
        self.statistic_of_order = 0
        self.side_length = 100
        # The history data in this partition
        self.points = []
        self.num_of_empty_drivers = 0

    def __str__(self):
        return 'partition id: %d, center (%f,%f)'%(self.partition_id, self.center_x, self.center_y)

    # The method can judge whether a point in this partition or not
    def is_in_this_partition(self, point):
        if fabs(point[0]-self.center_x) >= self.side_length or fabs(point[1]-self.center_y) >= self.side_length*sqrt(3)/2:
            return False
        elif self.side_length - fabs(point[0]-self.center_x) > fabs(point[1]-self.center_y)*sqrt(3)/3:
            return True

    # Add a history point
    def add_history_point(self,point):
        self.points.append(point)

###############
#  Test1
###############
# p = Partition(1,2.3, 3.4)
# print(p)
