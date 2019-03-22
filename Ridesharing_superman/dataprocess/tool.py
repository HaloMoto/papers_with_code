#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

def readwrite(input_file, output_file):
    date_1 = pd.read_csv(input_file, usecols=[1,2,5,6,7,8,9,10],encoding="utf-8")
    date_1.to_csv(output_file,index=False,encoding="utf-8")
    # print(list(date_1.columns))
    # print(date_1)
    # date_1.drop(columns=['VendorID', 'Store_and_fwd_flag', 'RateCodeID', 'Extra', 'MTA_tax', 'Tip_amount', 'Tolls_amount', 'Ehail_fee', 'Total_amount', 'Payment_type', 'Trip_type '])
    print(date_1.head())

readwrite("E:\data\green_data\green_tripdata_2014-05.csv","E:\data\green_data_processed\green_tripdata_2014-05.csv")