#! /usr/bin/env python
# -*- coding: utf-8 -*-

from scipy import *
import pylab

def f(p, pts):
    return sum(sum((p - pts) ** 2, axis=1) ** 0.5)

def fd(p, pts):
    dx = sum((p[0] - pts[:, 0]) / sum((p - pts) ** 2, axis=1) ** 0.5)
    dy = sum((p[1] - pts[:, 1]) / sum((p - pts) ** 2, axis=1) ** 0.5)
    s = (dx ** 2 + dy ** 2) ** 0.5
    dx /= s
    dy /= s
    return array([dx, dy])

def get_anchor_point(pts, x, t):
    for k in range(100):
        y = f(x, pts)
        xk = x - t * fd(x, pts)
        yk = f(xk, pts)
        if y - yk > 1e-1:
            x = xk
            y = yk
        elif yk - y > 1e-1:
            t *= 0.5
        else:
            break
    return x,y