#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql

# 连接历史数据库接口
def open_db_connection1():
    host_name = 'localhost'
    port_number = 3306
    user_name = 'root'
    password = '123456'
    database_name = 'trip_data'
    connection_object = pymysql.connect(host=host_name, port=port_number,
                                        user=user_name, passwd=password, db=database_name)
    return connection_object

# 连接司机路线和行程数据库的接口
def open_db_connection2():
    host_name = 'localhost'
    port_number = 3306
    user_name = 'root'
    password = '123456'
    database_name = 'girl'
    connection_object = pymysql.connect(host=host_name, port=port_number,
                                        user=user_name, passwd=password, db=database_name)
    return connection_object

# 关闭数据库连接的接口
def close_db_connection(connection_object):
    if connection_object is not None:
        connection_object.commit()
    connection_object.close()

