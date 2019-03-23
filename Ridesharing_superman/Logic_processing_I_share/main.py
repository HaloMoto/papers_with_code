#!/usr/bin/python
# -*- coding: utf-8 -*-

import config.Timeframe as Timeframe
import numpy as np

## 外部文件加载 ##
D = np.loadtxt("dist.txt")
T = np.loadtxt("time.txt")
Gd = np.loadtxt("Gd.txt")
Gt = np.loadtxt("Gt.txt")

## 加载配置文件 ##
# 模拟开始时间
starttime = Timeframe.starttime
# 模拟结束时间
endtime = Timeframe.endtime
#

## 订单分布 ##

## 司机数 ##
num_of_drivers = input('Please enter the number of drivers:')

## 订单池和司机池定义 ##
query_list = []
driver_list = []

## 生成司机池 ##

### 需要输出的一些变量定义 ###

""" 
判断订单池中的订单数有没有超过阈值O_thres,
如果是，则订单池先经过拼单算法处理，再将剩下的订单放入搜索算法中。
如果不是，则订单直接进入搜索算法处理。将拼单算法得到的合单进行路径规划。
将搜索算法得到的合单进行插入检查 ##
"""

