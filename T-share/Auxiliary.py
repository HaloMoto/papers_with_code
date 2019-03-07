#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def cal_distance(source, destination):
    return sum(map(lambda i, j: abs(i-j), source, destination))

def get_which_grid_the_location_belongs_to(location):
    return 20*(location[0]-1)+location[1]

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

##################################
#            Test1
##################################
# print(cal_distance([1,2], [3,4]))
# print(get_which_grid_the_location_belongs_to([2,2]))