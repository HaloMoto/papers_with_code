#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

# recursive function to obtain the path as a string
def obtainPath(i, j):
    if dist[i][j] == float("inf"):
        return " no path to "
    if parent[i][j] == i:
        return " "
    else:
        return obtainPath(int(i), int(parent[i][j])) + str(int(parent[i][j])+1) + obtainPath(int(parent[i][j]), int(j))


dist = np.loadtxt('dist.txt')
parent = np.loadtxt('route.txt')