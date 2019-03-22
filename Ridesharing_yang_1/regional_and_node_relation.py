#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

# Load partitions
with open('partitions.txt','rb') as f:
    partitions = pickle.load(f)

nodes_belong_to_which_partition = dict()

node_id = 1

with open("nodes_xy.txt","r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        x, y = [int(i) for i in lines.split()]
        for i in range(len(partitions)):
            if partitions[i].is_in_this_partition((x,y)):
                nodes_belong_to_which_partition[node_id] = i+1
                node_id += 1
                break
        else:
            print(x,y)
            print(node_id)
            node_id += 1

with open("anchor.txt","r") as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        x, y = [int(i) for i in lines.split()]
        for i in range(len(partitions)):
            if partitions[i].is_in_this_partition((x,y)):
                nodes_belong_to_which_partition[node_id] = i+1
                node_id += 1
                break

print(len(nodes_belong_to_which_partition))

# Save nodes and partitions relation
with open('nodes_belong_to_which_partition.txt','wb') as f:
    pickle.dump(nodes_belong_to_which_partition, f)

print(nodes_belong_to_which_partition)