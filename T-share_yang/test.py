#! /usr/bin/env python
# -*- coding: utf-8 -*-

from cal_distance import cal_distance
from math import cos,pi
from scipy import *
import numpy as np

def run():
    # # test1
    # point1_lat = 40.663759
    # point2_lat = 40.663759
    # point1_lon = -73.927997
    # point2_lon = -73.907997
    # # test2
    # point1_lat = 40.663759
    # point2_lat = 40.645793
    # point1_lon = -73.927997
    # point2_lon = -73.927997
    # test3
    point1_lat = 40.663759
    point2_lat = 40.663759
    point1_lon = -73.929870
    point2_lon = -73.906124
    Distance = cal_distance(lat1=point1_lat, lon1=point1_lon, lat2=point2_lat, lon2=point2_lon)
    distance = Distance.twopoint_distance()
    print(distance)


if __name__ == '__main__':
    run()
    print(1.11111111111111>=1.11111111111111)
    a = 1
    print(a != None)
    print(1.1*1000)
    b = 1
    b += 1
    print(b)
    c = [1,2,3,4]
    print(sum(c))
    d = [(1,2),(2,3),(3,4)]
    print(sum(d, axis=0))
    e = [5,6]
    d = array(d)
    e = array(e)
    print(e-d)
    str = "123,456,789"
    a1,a2,a3 = str.split(",")
    print(a1,a2,a3)
    print(int(a1)+int(a2))
    # print(str.split(","))
    b1 = 1.2
    b2 = 1.7
    print(int(b1), int(b2))
    c1 = [[1,2,3],
          [4,5,6],
          [7,8,9]]
    c1 = np.array(c1)
    print(c1[0:2, 1:3])
    d1 = c1[0:2]
    print(d1[:, 1:3])
    print(c1[1][1])

