#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' A Large-Service Dynamic Taxi Ridesharing Service '

__author__ = 'Xiangyuan Yang'

class Query(Object):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination