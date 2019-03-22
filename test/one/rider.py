#! /usr/bin/env python
# -*- coding: utf-8 -*-

class rider(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "lat: %f, lon:%f"%(self.lat, self.lon)