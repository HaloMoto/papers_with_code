#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sys
from Driver import Driver

argv1 = sys.argv[1]
f = open("inp"+argv1+".txt","w")
f.write('400\n')#no. of nodes
f.write('1520\n')#no. of arcs
for i in range(1,21):
    for j in range(1,20):
        f.write(str(20*(i-1)+j) + ' ' + str(20*(i-1)+j+1) + ' ' + str(1)+'\n')
        f.write(str(20*(i-1)+j+1) + ' ' + str(20*(i-1)+j) + ' ' + str(1)+'\n')
        f.write(str(20*(j-1)+i) + ' ' + str(20*j+i) + ' ' + str(1)+'\n')
        f.write(str(20*j+i) + ' ' + str(20*(j-1)+i) + ' ' + str(1)+'\n')
f.close()

argv2 = sys.argv[2]
f = open("inp"+argv2+".txt","w")
with open("inp"+argv1+".txt","r") as file_to_read:
    num_of_nodes = int(file_to_read.readline())
    num_of_arcs = int(file_to_read.readline())
    f.write(str(num_of_nodes)+"\n")
    f.write(str(num_of_arcs)+"\n")
    print(num_of_nodes, num_of_arcs)
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        start, end, length = [int(i) for i in lines.split()]
        f.write(str(start) + ' ' + str(end) + ' ' + str(int(length/Driver.speed))+'\n')
f.close()