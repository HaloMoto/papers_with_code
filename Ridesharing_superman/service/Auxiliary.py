#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np

def deg2rad(deg):
    return deg * (math.pi / 180)

def coord2lonlat(coord, LL):
    R = 6371.393
    dlon = coord[0] / (R*1000*math.cos(deg2rad(LL[1]))*2*3.1415926/360)
    dlat = coord[1] / 111000
    return (LL[0]+dlon, LL[1]+dlat)

# 获得两点的最短路径
def obtainPath(i, j):
    if dist[i][j] == float("inf"):
        return " no path to "
    if parent[i][j] == i:
        return " "
    else:
        return obtainPath(int(i), int(parent[i][j])) + str(int(parent[i][j])+1) + obtainPath(int(parent[i][j]), int(j))

dist = np.loadtxt('../data/dist.txt')
parent = np.loadtxt('../data/route.txt')