# -*- coding: utf-8 -*-

from Auxiliary import *
import networkx as nx
from networkx.algorithms.matching import max_weight_matching

def exact_join(rider_set, driver_set, PI_0):
    G = nx.Graph()
    C = candidate_set_gen(rider_set, driver_set, PI_0)
    for tup in C:
        shared_route_percentage = get_shared_route_percentage(tup[0], tup[1])
        if is_satisfied_with_shared_requirement(tup[0].sharing_requirement, shared_route_percentage):
            G.add_edge(tup[0], tup[1], weight=shared_route_percentage)
    matching = max_weight_matching(G)
    return matching

def candidate_set_gen(rider_set, driver_set, PI_0):
    C = set()
    for r_j in rider_set:
        delta_j_PI_0 = (1/float(PI_0) - 1) * cal_shortest_route_distance(r_j.source, r_j.destination)
        D_j_source = set()
        D_j_destination = set()
        for d_i in driver_set:
            if cal_shortest_route_distance(d_i.source, r_j.source) <= delta_j_PI_0:
                D_j_source.add(d_i)
            if cal_shortest_route_distance(d_i.destination, r_j.destination) <= delta_j_PI_0:
                D_j_destination.add(d_i)

        for d_i in D_j_source.intersection(D_j_destination):
            C.add((d_i, r_j))

    return C



