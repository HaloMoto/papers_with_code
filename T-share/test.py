#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import random
from Auxiliary import obtainPath
import numpy as np

a = [1,2,3]
if not a:
    print("hello world!")
print(int(len(a)/2))

for i in range(1,4):
    print(i)

for i in range(5):
  for j in range(5):
    for k in range(5):
      if i == j == k == 3:
        break
      else:
        print(i, '----', j, '----', k)
    else:
        print(k)
    break
  else: continue
  break

for i in range(5):
    if True:
        if i == 2:
            continue
    print(i)

l = [1,2,3,4]
del l[0]
print(l)

print(- 1 / 2)

d = datetime.datetime.now()
print(d)
d = d + datetime.timedelta(seconds=random.randint(1,3))
print(d)

# for i in range(0,V):
#     for j in range(0,V):
#         route_temp = str(i+1) + obtainPath(i,j) + str(j+1)
#         route[i][j] = route_temp.split()
route_temp = str(4) + obtainPath(3,7) + str(8)
print(route_temp.split())

l1 = [1,2,3]
l2 = [4,5,6]

print(l1)
l1.extend(l2)
print(l1)
del l1[1]
print(l1)
a = l1[3]
l1.remove(a)
print(l1)
l1.append(3)
print(l1)
b = l1[4]
l1.remove(b)
print(l1)
for i in l1:
    if i == 1:
        l1.remove(i)
print(l1)

date_1 = datetime.datetime.now()

date_2 = datetime.datetime.now() + datetime.timedelta(seconds=3)

print((date_2 - date_1).seconds+1)

print(date_2 < date_1)

T = np.loadtxt('time.txt')

print(T[1][12])
print(T[12][1])

l3 = [1,2,3,4,5,6]
for i in l3:
    if i == 4:
        print(i)
        l3.remove(i)
print(l3)

del l3[0]
print(l3[0])

print(13%5)

print(int(1.5))

for i in range(0,10):
    if i > 10:
        break
    else:
        print('hello world!')

for i in range(0):
    for j in range(1,1):
        print('hh')
        break;
    else:
        print('ll')
        continue
    break
else:
    print('dd')