import numpy as np
import pickle
from partition import Partition

x=np.random.random(10)*10
y=np.random.random(10)*20

X=np.vstack([x,y])
print(X)
#方法一：根据公式求解
sk=np.var(X,axis=0,ddof=1)
d1=np.sqrt(((x - y) ** 2 /sk).sum())
print("d1:",d1)

#方法二：根据scipy库求解
from scipy.spatial.distance import pdist
d2=pdist(X,'seuclidean')
print("d2:",d2)

a = 1
a += 1
print(a)

with open('partitions.txt','rb') as f:
    partitions = pickle.load(f)



hot_index = []
hot_index.append(0)
for partition in partitions:
    hot_index.append(hot_index[-1]+partition.hot_index)
    print("hot_index:", partition.hot_index)
print(hot_index)
print(len(hot_index))

for i in range(5):
    for j in range(5):
        for k in range(5):
            if i == 3:
                break
            print(i, j, k)
        else:continue
        break
    print("hello")

# Load nodes_belong_to_which_partition.txt
with open('nodes_belong_to_which_partition.txt','rb') as f:
    nodes_belong_to_which_partition = pickle.load(f)

print(nodes_belong_to_which_partition)

a = 1
b = 2
print("haha",a/b)

l = []
if 1 == 1 and l:
    print(1234)