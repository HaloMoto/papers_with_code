#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np
from dao.dbconnect import *
import datetime

class Driver:

    # 车容量，可以坐多少个乘客
    capacity = 4
    # 车速，m/s
    speed = 25

    def __init__(self, driver_id):
        # 司机当前位置，模拟过程中，随机分配
        self.cur_location = random.randint(1,430)
        # 司机id
        self.driver_id = driver_id
        # 车上已有乘客数
        self.num_of_occupied_position = 0
        # 当前行程安排
        self.cur_schedule = []
        # 当前行驶路线
        self.route = []
        # 司机经过某个点多长时间
        self.assist_t = 0
        # 接单数
        self.number_of_order = 0
        # 载客总行驶时间
        self.total_time_traveled = 0
        # 载客总行驶距离
        self.total_distance_traveled = 0
        # 无共享的总行驶距离
        self.total_distance_no_sharing = 0
        # 连接数据库
        self.cnn = open_db_connection2()

    # 打印司机对象
    def __str__(self):
        return 'The driver id: %d, current location: (%d, %d), number of occupied position: %d.'%(self.driver_id, self.cur_location[0], self.cur_location[1], self.num_of_occupied_position)

    # 析构函数，释放数据库连接
    def __del__(self):
        close_db_connection(self.cnn)

    # 增加/减少乘客
    def add_passenger(self, num_of_passenger):
        self.num_of_occupied_position = self.num_of_occupied_position + num_of_passenger
        return self.num_of_occupied_position

    # 得到剩下的乘客数
    def get_num_of_seats_remaining(self):
        return Driver.capacity - self.num_of_occupied_position

    # 判断是否到达了行程安排中的第一个点
    def does_it_reach_the_first_point_in_the_schedule(self, t_cur):
        if self.cur_schedule:
            while True:
                if self.cur_schedule and self.cur_location == self.cur_schedule[0][0]:
                    if self.cur_schedule[0][2] == 1:
                        self.add_passenger(-1)
                        # # 插入路程安排到数据库
                        # # 使用cursor()方法获取操作游标
                        # cursor = self.cnn.cursor()
                        # # SQL插入语句
                        # q = "insert into schedule(conditions,driverid,latitude,longitude,remain,time) values (" + 1 + "," + self.driver_id + "," + LQ[self.cur_location-1][1] + "," + LQ[self.cur_location-1][0] + "," + self.get_num_of_seats_remaining() + "," + t_cur + ")"
                        # try:
                        #     # 执行sql语句
                        #     cursor.execute(q)
                        #     # 提交到数据库执行
                        #     self.cnn.commit()
                        # except:
                        #     # Rollback in case there is any error
                        #     self.cnn.rollback()
                        del self.cur_schedule[0]
                    else:
                        # # 插入路程安排到数据库
                        # # 使用cursor()方法获取操作游标
                        # cursor = self.cnn.cursor()
                        # # SQL插入语句
                        # q = "insert into schedule(conditions,driverid,latitude,longitude,remain,time) values (" + 0 + "," + self.driver_id + "," + LQ[self.cur_location-1][1] + "," + LQ[self.cur_location-1][0] + "," + self.get_num_of_seats_remaining() + "," + t_cur + ")"
                        # try:
                        #     # 执行sql语句
                        #     cursor.execute(q)
                        #     # 提交到数据库执行
                        #     self.cnn.commit()
                        # except:
                        #     # Rollback in case there is any error
                        #     self.cnn.rollback()
                        del self.cur_schedule[0]
                else:
                    break

    # 在t秒之后，判断司机能否到达行驶路程的下一个点
    def reach_the_next_point(self, t, t_cur):
        t_cur_ = t_cur + datetime.timedelta(seconds=t)
        if not self.route:
            return
        while True:
            t = t + self.assist_t
            if not self.route:
                break
            if t * self.speed > D[self.cur_location-1][int(self.route[0])-1] / 2:
                old_location = self.cur_location
                # # 运行数据保存模块
                # cursor = self.cnn.cursor()
                # q = "insert into route(driverid,latitude,longitude,time) values (" + self.driver_id + "," + LQ[old_location-1][1] +"," + LQ[old_location-1][0] + "," + t_cur + ")"
                # try:
                #     # 执行sql语句
                #     cursor.execute(q)
                #     # 提交到数据库执行
                #     self.cnn.commit()
                # except:
                #     # Rollback in case there is any error
                #     self.cnn.rollback()
                self.cur_location = int(self.route[0])
                del self.route[0]

                self.assist_t = (self.speed * t - D[old_location-1][self.cur_location-1]) / self.speed
                self.does_it_reach_the_first_point_in_the_schedule(t_cur_)
                t = 0
            else:
                self.assist_t = t
                break

D = np.loadtxt('../data/dist.txt')
LQ = np.loadtxt('../data/location_query.txt')
