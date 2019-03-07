#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from rtree import index
#
# idx = index.Index()
#
# left, bottom, right, top = (0.0, 0.0, 1.0, 1.0)
# idx.insert(0, (left, bottom, right, top))
# # intersection
# print(list(idx.intersection((1.0, 1.0, 2.0, 2.0))))
# print(list(idx.intersection((1.0000001, 1.0000001, 2.0, 2.0))))
# # Nearest Neighbors
# idx.insert(1, (left, bottom, right, top))
# print(list(idx.nearest((1.0000001, 1.0000001, 2.0, 2.0),1)))
# # index.insert(id=id, bounds=(left, bottom, right, top), obj=42)
# # print([n.object for n in idx.intersection((left, bottom, right, top), objects=True)])
# file_idx = index.Rtree('rtree')
# file_idx.insert(1, (left, bottom, right, top))
# file_idx.insert(2, (left - 1.0, bottom - 1.0, right + 1.0, top + 1.0))
# print([n for n in file_idx.intersection((left, bottom, right, top))])
# p = index.Property()
# p.dat_extension = 'data'
# p.idx_extension = 'index'
# file_idx = index.Index('rtree', properties=p)

from rtree import index
p = index.Property()
p.dimension = 3
p.dat_extension = 'data'
p.idx_extension = 'index'
idx3d = index.Index('3d_index', properties=p)
idx3d.insert(1, (0, 0, 60, 60, 23.0, 62.0))
print(list(idx3d.intersection( (-1, -1, 62, 62, 22, 63))))