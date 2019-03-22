#! /usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt

def cal_two_point_distance(a, b):
    return sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

f = open("anchor_and_nearest_node.txt", "w")
nodes = []
anchors = []
with open("nodes_xy.txt", "r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        x, y = [int(i) for i in lines.split()]
        nodes.append((x,y))

with open("anchor.txt","r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        x, y = [int(i) for i in lines.split()]
        anchors.append((x,y))

for i in range(len(anchors)):
    min = 0
    min_value = cal_two_point_distance(anchors[i], nodes[0])
    for j in range(1,len(nodes)):
        value = cal_two_point_distance(anchors[i],nodes[j])
        if value < min_value:
            min = j;
            min_value = value
    f.write(str(i+1+245) + " " + str(min+1) + " " + str(int(min_value)) + '\n')
    f.write(str(min + 1) + " " + str(i + 1 + 245) + " " + str(int(min_value)) + '\n')
f.close()