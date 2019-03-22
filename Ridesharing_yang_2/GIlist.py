"""
creates output matrices Gd and Gt that give order of nodes based on closeness for all nodes
run using:
python GIlist.py <x>
<x> is dist or time, for spatial or temporal sorting respectively
"""
import numpy as np

# use the dist or time matrice created by Floyd-Warshall algorithm
D = np.loadtxt('dist.txt')
T = np.loadtxt('time.txt')
# Get the distance matrix between anchors is obtained by intercepting the matrix
D = D[245:420,245:420]
T = T[245:420,245:420]
Gd = np.zeros([175, 175])
Gt = np.zeros([175, 175])
for i in range(1,176):
    Gd[i-1] = np.argsort(D[i-1], kind='quicksort', order=None)+1
    Gt[i-1] = np.argsort(T[i-1], kind='quicksort', order=None)+1

# Save output
np.savetxt('Gd.txt', Gd, fmt='%-3.0f')
np.savetxt('Gt.txt', Gt, fmt='%-3.0f')