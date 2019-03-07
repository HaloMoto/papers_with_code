# -*- coding: utf-8 -*-

from Driver import Driver
from Rider import Rider
import networkx as nx
from networkx.algorithms.matching import max_weight_matching
from Auxiliary import get_shared_route_percentage
import matplotlib.pyplot as plt

driver = Driver()
rider = Rider()
shared_route_percentage = get_shared_route_percentage(driver, rider)
G = nx.Graph()
G.add_edge(driver, rider, weight=shared_route_percentage)
S = max_weight_matching(G)
print(S)
matching = nx.bipartite.maximum_matching(G)
print(matching)