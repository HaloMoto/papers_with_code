#! /usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt
from partition import Partition
import dbconnect
from cal_distance import cal_distance
from Constant import LL
from cal_anchor import *
import pickle

partitions = []

for i in range(7):
    for j in range(13):
        partitions.append(Partition(25*i+j+1, 2*i*150, 100*sqrt(3)*j))
    for j in range(12):
        partitions.append(Partition(25*i+13+j+1, (2*i+1)*150, 100*sqrt(3)*j+50*sqrt(3)))

connection_object = dbconnect.open_db_connection()
cursor = connection_object.cursor()
# the query statement get all data in the rectangular range
q = "select Pickup_longitude,Pickup_latitude from trip where Pickup_longitude <= -73.906124 and Pickup_longitude >= -73.929870 and Pickup_latitude >= 40.645793 and Pickup_latitude <= 40.663759"
cursor.execute(q)
first_record = cursor.fetchone()
# print(first_record[0])
if cursor != None:
    for point in cursor:
        for partition in partitions:
            distance1 = cal_distance(lat1=point[1], lon1=point[0], lat2=point[1], lon2=LL[0])
            distance2 = cal_distance(lat1=point[1], lon1=point[0], lat2=LL[1], lon2=point[0])
            # point = (distance1.twopoint_distance()*1000, distance2.twopoint_distance()*1000)
            # Calculate the distance of two points and the unit is meter
            point_temp = (distance1.twopoint_distance(), distance2.twopoint_distance())
            # print(point_temp)
            # print(partition.is_in_this_partition(point))
            if partition.is_in_this_partition(point_temp):
                partition.add_history_point(point_temp)
                # print(len(partition.points))
                break
    sum = 0
    for partition in partitions:
        sum = sum + len(partition.points)
        print(len(partition.points))
    # print(sum)
    for partition in partitions:
        partition.hot_index = len(partition.points)
        print(partition.hot_index)

    # Calculate the anchor point for each partition
    for partition in partitions:
        if not partition.points:
            partition.anchor = [partition.center_x, partition.center_y]
        elif len(partition.points) == 1:
            partition.anchor = list(partition.points[0])
        elif len(partition.points) == 2:
            partition.anchor = [(partition.points[0][0]+partition.points[1][0])/2, (partition.points[0][1]+partition.points[1][1])/2]
        else:
            partition.anchor,min_distance = get_anchor_point(array(partition.points), array([0,0]), 1000)
            print("The anchor point:", partition.anchor, "  the min distance:", min_distance)

# Save anchors for each partition
f = open("anchor.txt", "w")
for partition in partitions:
    f.write(str(int(partition.anchor[0])) + " " + str(int(partition.anchor[1])) + "\n")
f.close()

# Save partitions
with open('partitions.txt','wb') as f:
    pickle.dump(partitions, f)

#Calculate the length of each edge in map
nodes = []
with open("node.txt","r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        longitude, latitude, node_id = lines.split(",")
        longitude = float(longitude)
        latitude = float(latitude)
        node_id = int(node_id)
        nodes.append((longitude, latitude))

print(len(nodes))
print(nodes[244])

f = open("edge_length.txt","w")
with open("edge.txt","r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        start, end = [int(i) for i in lines.split(",")]
        # print(start, end)
        # print(nodes[end-1])
        distance_temp = cal_distance(lat1=nodes[start-1][1], lon1=nodes[start-1][0], lat2=nodes[end-1][1], lon2=nodes[end-1][0])
        f.write(str(start) + ' ' + str(end) + ' ' + str(int(distance_temp.twopoint_distance())) + '\n')
f.close()

# Converting points represented by latitude and longitude to coordinate positions
f = open("nodes_xy.txt", "w")
for node in nodes:
    distance_x = cal_distance(lat1=node[1], lon1=LL[0], lat2=node[1], lon2=node[0])
    distance_y = cal_distance(lat1=LL[1], lon1=node[0], lat2=node[1], lon2=node[0])
    f.write(str(int(distance_x.twopoint_distance())) + " " + str(int(distance_y.twopoint_distance())) + '\n')
f.close()
#
# # print(partitions)
# # print(len(partitions))

