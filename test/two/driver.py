#! /usr/bin/env python
# -*- coding: utf-8 -*-

class driver(object):
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "id: %d, lat: %f, lon: %f"%(self.id, self.lat, self.lon)