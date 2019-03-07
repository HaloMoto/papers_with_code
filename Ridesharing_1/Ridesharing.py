#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import radians,cos,sin,asin,sqrt
import requests
import json

def dbConnect():
    return

def dbClose():
    return

# The function get all records within 5 minutes
def get_each_pool():
    return

def dbscan_cluster():
    return

def kmneas_cluster():
    return

def get_cluster_points():
    return

#The haversine formula
def haversine(lonlat1, lonlat2):
    lat1, lon1 = lonlat1
    lat2, lon2 = lonlat2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def get_distance(plat, plong, dlat, dlong):
    requestString = 'http://localhost:8989/route?point=' + str(plat) + '%2C' + str(plong) + '&point=' + str(
        dlat) + '%2C' + str(dlong) + '&vehicle=car'
    r = requests.get(requestString)

    res = json.loads(r.text)

    return_list = []
    if ('paths' in res):
        return_list.append(res['paths'][0]['distance'])
        return_list.append(res['paths'][0]['time'])
        return return_list
    else:
        return_list.append(-250)
        return_list.append(-250)
        return return_list

# To get the total travel distance before ridesharing
def get_without_ridesharing_distance(coord_list):
    return

# To get the total travel distance after ridesharing
def get_with_ridesharing_distance(carassign, carcount):
    return

def get_RSP(route1_source, route1_dest, route2_source, route2_dest):
    return



print(haversine([47, 78], [48, 79]))
