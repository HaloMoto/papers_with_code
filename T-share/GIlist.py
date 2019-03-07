"""
creates output matrices Gd and Gt that give order of nodes based on closeness for all nodes
run using:
python GIlist.py <x>
<x> is dist or time, for spatial or temporal sorting respectively
"""
import numpy as np
import sys

argv = sys.argv[1]
D = np.loadtxt(argv+'.txt')#use the dist or time matrice created by Floyd-Warshall algorithm
Gd = np.zeros([400,400])
for i in range(1,401):
    Gd[i-1] = np.argsort(D[i-1], kind='quicksort', order=None)+1
if(argv=='dist'):
    np.savetxt('Gd.txt', Gd, fmt='%-3.0f')
elif(argv=='time'):
    np.savetxt('Gt.txt', Gd, fmt='%-3.0f')
