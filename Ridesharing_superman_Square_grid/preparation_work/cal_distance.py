#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math

class cal_distance(object):
    def __init__(self, **kwargs):
        self.lat1 = kwargs.get('lat1')
        self.lon1 = kwargs.get('lon1')
        self.lat2 = kwargs.get('lat2')
        self.lon2 = kwargs.get('lon2')

    def twopoint_distance(self):
        R = 6371.393
        dlat = self.deg2rad(self.lat2 - self.lat1)
        dlon = self.deg2rad(self.lon2 - self.lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(self.deg2rad(self.lat1)) * math.cos(self.deg2rad(self.lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c * 1000

    def deg2rad(self, deg):
        return deg * (math.pi / 180)