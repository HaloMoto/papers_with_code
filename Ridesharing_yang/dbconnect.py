#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

# Function to open the database connection
def open_db_connection():
    host_name = 'localhost'
    port_number = 3306
    user_name = 'root'
    password = '123456'
    database_name = 'trip_data'
    connection_object = pymysql.connect(host=host_name, port=port_number,
                                        user=user_name, passwd=password, db=database_name)
    return connection_object

# Function to close the database connection
def close_db_connection(connection_object):
    if connection_object is not None:
        connection_object.commit()
    connection_object.close()