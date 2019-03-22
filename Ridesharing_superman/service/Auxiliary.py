#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math

def deg2rad(deg):
    return deg * (math.pi / 180)

def coord2lonlat(coord, LL):
    R = 6371.393
    dlon = coord[0] / (R*1000*math.cos(deg2rad(LL[1]))*2*3.1415926/360)
    dlat = coord[1] / 111000
    return (LL[0]+dlon, LL[1]+dlat)