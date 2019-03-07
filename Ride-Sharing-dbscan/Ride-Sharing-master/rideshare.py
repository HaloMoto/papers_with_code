import datetime
import json

import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import requests
from sklearn.cluster import DBSCAN
from mysql.connector import errorcode
from scipy.cluster.vq import kmeans2, whiten
from math import radians,sin,cos,asin,sqrt,ceil

import Timeframe


# Since downloaded dataset is in .csv file, create a new table in mysql database with the same field names,
# and load all the data into the created table
# Our aim is to work with single source pickup (JFK), for that we filtered data with pickup location only
# as JFK within 2 mile radius
# The set of below commented code should be run only for the first time when you run the program.


##  QUERIES TO EXECUTE FROM PYTHON IDLE or PYTHON IDE

# query = "CREATE TABLE trip_data_11(medallion VARCHAR(20),hack_license VARCHAR(20)," \
#         "vendor_id varchar(10),rate_code INT,store_and_fwd_flag varchar(5),pickup_datetime datetime" \
#         " , dropoff_datetime datetime,passenger_count INT,trip_time_in_secs INT," \
#         "trip_distance DOUBLE,pickup_longitude DECIMAL(20,10),pickup_latitude DECIMAL(20,10)," \
#         "dropoff_longitude DECIMAL(20,10),dropoff_latitude DECIMAL(20,10))"
# cursor.execute(query)

# load_query = "LOAD DATA LOCAL INFILE '/Users/Nivetha/Downloads/trip_data_8.csv' " \
#              "INTO TABLE tripdata FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES"

# jfk_query = "CREATE TABLE jfk_data_12 AS SELECT *, ( 3959 * acos ( cos ( radians(40.645574) )" \
#             " * cos( radians( pickup_latitude ) ) * cos( radians( pickup_longitude ) - radians(-73.784866) )" \
#             " + sin ( radians(40.645574) ) * sin( radians( pickup_latitude ) ) ) ) " \
#             "AS distance FROM trip_data_12 HAVING distance < 2 and passenger_count<=4"
# cursor.execute(jfk_query)


# Implementation of K-means clustering and Trip Matching Algorithm

###### OR #####

"""

Queries to Execute in MySQL workbench

CREATE TABLE trip_data1_2010(medallion VARCHAR(20),hack_license VARCHAR(20), vendor_id varchar(10),rate_code INT,
store_and_fwd_flag varchar(5),pickup_datetime datetime, dropoff_datetime datetime,passenger_count INT,trip_time_in_secs INT,
trip_distance DOUBLE,pickup_longitude DECIMAL(20,10),pickup_latitude DECIMAL(20,10), dropoff_longitude DECIMAL(20,10),
dropoff_latitude DECIMAL(20,10))

LOAD DATA LOCAL INFILE 'C:/Users/rashmi/Desktop/DBMS/Project/FOIL2010/FOIL2010/trip_data_1/trip_data_1.csv' 
INTO TABLE trip_data1_2010 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES


CREATE TABLE jfk_data1_2010 AS SELECT *, ( 3959 * acos ( cos ( radians(40.645574) ) * cos( radians( pickup_latitude ) ) 
* cos( radians( pickup_longitude ) - radians(-73.784866) ) + sin ( radians(40.645574) ) * sin( radians( pickup_latitude ) ) ) )
 AS distance FROM trip_data1_2010 HAVING distance < 2 and passenger_count<=4
 

 
SET GLOBAL innodb_buffer_pool_size=402653184; ### if Error comes : ERROR: The total number of locks exceeds the lock table size Error Code: 1206
 
"""

def kmeanscluster(starttime , endtime):
    global numpool

    # Connecting to MySQL Database where the database is stored using MySQL Connector package

    try:
        cnn = mysql.connector.connect(
            user='root',
            password='123456',
            host='localhost',
            port=3306,
            database='trip_data')
        # print("it works")
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_CHANGE_USER_ERROR:
            print("somethind os wrong with username and password")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("database doesn't exist")
        else:
            print(e)

    cursor = cnn.cursor()

    # This function is to select a particular pool's source and its destination points, Total
    # number of records and passenger count for each trip

    def selecteachpool():
        # This query is to select fields with filtering data for a particular pool.
        query = "Select tripid, Dropoff_longitude, Dropoff_latitude, passenger_count from trip WHERE Lpep_pickup_datetime >= '" + str(starttime) + "'and Lpep_pickup_datetime < '" + str(endtime) + "'"
        cursor.execute(query)
        result_set = cursor.fetchall()
        coord_list = []
        passenger_count = []
        for row in result_set:
            temp = [float(row[1]), float(row[2])]
            coord_list.append(temp)

        for row in result_set:
            passenger_count.append(int(row[3]))

        recordcount = 0
        for outerlist in coord_list:
            recordcount += 1
        return coord_list, passenger_count

    # Returns the list of dropoff latitude and longitude points
    def getcoord_list():
        return coord_list

    # calculating value of k to run k-means clustering Algorithm
    def getkvalue(recordcount):
        kvalue = (int)(ceil(recordcount / 4))
        # print("No of records:", count)
        return kvalue

    # Run K-means clustering Algorithm using scipy-cluster package.
    def kmeanscluster(coord_list, k_value):
        coordinates = np.array(coord_list)
        return kmeans2(whiten(coordinates), k_value, missing='warn',)

    def haversine(lonlat1, lonlat2):
        lat1, lon1 = lonlat1
        lat2, lon2 = lonlat2
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    # 使用密度聚类算法，将距离近的点聚集在一个类中
    def dbscancluster(coord_list):
        coord_list_source = np.array(coord_list)
        # print(coord_list_source)
        db = DBSCAN(eps=0.9, min_samples=3, metric=lambda a, b:haversine(a, b))
        db.fit(np.array(coord_list_source))
        n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
        # print("coord_list_length:",len(coord_list))
        # print("labels_length:",len(db.labels_))
        # print(db.labels_)
        # print(db.core_sample_indices_)
        # print(len(db.core_sample_indices_))
        # print(db.components_)
        # print("components:",len(db.components_))
        print("n_clusters:",n_clusters_)
        return n_clusters_, db.labels_


    # To plot the k-means clutering results in form of graph
    def plotkmeanscluster(coord_list, labels):
        coordinates = np.array(coord_list)
        plt.scatter(coordinates[:, 0], coordinates[:, 1], c=labels, iter = 5)
        plt.show()

    # To get the cluster points after running k-means clustering Algorithm
    def getclusterpoints_dbscan(coord_list, labels, num_clusters):
        clusterpt = [0 for x in range(num_clusters)]
        for i in range(0, num_clusters):
            clusterpt[i] = []
        listitem = 0
        for i in labels:
            if i == -1:
                listitem = listitem + 1
                continue
            clusterpt[i].append(coord_list[listitem])
            listitem = listitem + 1
        return clusterpt

    # To get the cluster points after running k-means clustering Algorithm
    def getclusterpoints(coord_list, labels, kvalue):
        clusterpt = [0 for x in range(kvalue)]
        for i in range(0, kvalue):
            clusterpt[i] = []
        listitem = 0
        for i in labels:
            clusterpt[i].append(coord_list[listitem])
            listitem = listitem + 1
        return clusterpt

    # Print those cluster points(dropoff latitudes and dropoff longitudes)
    def printclusterpoints(clusterpt, kvalue):
        print("\nkmeans clustering result \n")
        for i in range(0, kvalue):
            print("cluster number:", i, clusterpt[i])

    # After clustering is formed, merge trips with maximum capacity of 4
    def carassignment(clusterpt, kvalue):
        carassign = []
        carcount = -1
        for i in range(0, kvalue):
            for j in range(0, len(clusterpt[i])):
                if (j % 4 == 0):
                    carassign.append([])
                    carcount = carcount + 1
                    carassign[carcount].append(clusterpt[i][j])
                else:
                    carassign[carcount].append(clusterpt[i][j])
        return carassign, carcount + 1

    # Get the dropoff latitude and longitude points after we merged the trips
    def getcarassignment():
        return carassign, carcount

    # print trips after we merged the trips
    def printridesshared(carassign, carcount):
        print("\nRide shared cars and its destination\n")
        for i in range(0, carcount):
            print("car number:", i, carassign[i])

    # To get distance and Time between two latitude and longitude points using graphhopper API

    def getDistance(plat, plong, dlat, dlong):
        requestString = 'http://localhost:8989/route?point=' + str(plat) + '%2C' + str(plong) + '&point=' + str(
            dlat) + '%2C' + str(dlong) + '&vehicle=car'
        r = requests.get(requestString)

        res = json.loads(r.text)

        return_list = []
        if ('paths' in res):
            return_list.append(res['paths'][0]['distance'])
            return_list.append(res['paths'][0]['time'])
            return return_list
        else:
            return_list.append(-250)
            return_list.append(-250)
            return return_list

    # To get the total travel distance before ridesharing
    def getwithoutridesharingdistance(coord_list):
        # Initialize some global and local variables
        global tnormaldist
        global wolength
        wolength = wolength + len(coord_list)
        normaldistance = 0
        # Calculate  distance between JFK and all the destination points
        for i in range(0, len(coord_list)):
            dist = getDistance(40.645574, -73.784866, coord_list[i][1], coord_list[i][0])
            normaldistance = normaldistance + dist[0]
        normaldistance = normaldistance / 1000
        tnormaldist = tnormaldist + normaldistance  # Sum up all the trip distances
        print("\nDistance without ride sharing:", normaldistance, "km")
        return normaldistance

    # To get the total travel distance After ridesharing
    def getwithridesharingdistance(carassign, carcount):
        # Initialize some global and local variables
        global tridesharedist
        global wlength
        wlength = wlength + len(carassign)
        ridesharedist = 0
        # Calculate  distance travelled by trips after ridesharing
        # For that, we took JFK as source and First destination point as destinaation
        # After first passenger dropped off, Keep Previous Destination point as source and current destination
        # point as destination and repeat the process till all the passengers for a trip dropped off.
        for i in range(0, carcount):
            initlat = 40.645574
            initlog = -73.784866
            for j in range(0, len(carassign[i])):
                if (j != 0):
                    initlat = carassign[i][j - 1][1]
                    initlog = carassign[i][j - 1][0]
                distance = getDistance(initlat, initlog, carassign[i][j][1], carassign[i][j][0])
                ridesharedist = ridesharedist + distance[0]

        ridesharedist = ridesharedist / 1000
        tridesharedist = tridesharedist + ridesharedist  # Sum up all the trip distances
        print("Distance with ride sharing:", ridesharedist, "km")
        return ridesharedist

    # This function returns the distance saved in percentage
    def getsaveddistance(normaldistance, ridesharedist):
        global totaldistance
        distancesaved = (1 - (ridesharedist / normaldistance)) * 100
        print(distancesaved)
        totaldistance = totaldistance + distancesaved

    coord_list, passenger_count = selecteachpool()
    if (len(coord_list) < 4): # Skipping pools where the trips are too small or zero
        return
    db_core_num, db_labels = dbscancluster(coord_list)
    clusterpt_db = getclusterpoints_dbscan(coord_list, db_labels, db_core_num)
    norm_sum = 0
    rideshare_sum = 0
    for i in range(db_core_num):
        if len(clusterpt_db[i]) < 2:
            continue
        kvalue = getkvalue(len(clusterpt_db[i]))
        meanpoints, labels = kmeanscluster(clusterpt_db[i],kvalue)
        # plotkmeanscluster(clusterpt_db[i],labels)
        clusterpt_kmeans = getclusterpoints(clusterpt_db[i], labels, kvalue)
        # printclusterpoints(clusterpt, kvalue)
        carassign, carcount = carassignment(clusterpt_kmeans, kvalue)
        # printridesshared(carassign, carcount)
        normaldistance = getwithoutridesharingdistance(clusterpt_db[i])
        ridesharedist = getwithridesharingdistance(carassign, carcount)
        norm_sum = norm_sum + normaldistance
        rideshare_sum = rideshare_sum + ridesharedist
        # getsaveddistance(normaldistance, ridesharedist)
        numpool = numpool + 1  # To calculate the total number of pools
    print((1 - (rideshare_sum / norm_sum)) * 100)

    cnn.commit()
    cursor.close()
    cnn.close


# Initializing some global variables

starttime = Timeframe.starttime
endtime = Timeframe.endtime
numpool = 0
totaldistance = 0
tnormaldist = 0
tridesharedist = 0
wolength = 0
wlength = 0

programstarttime = datetime.datetime.now() # Record the system time before start of the Algorithm
print("\nAlgorithm start time:",programstarttime)

# Run the Algorithm for each pool window until the end time.

while endtime <= Timeframe.untildatetime:
    print("\npool : ",starttime, "-",endtime)
    kmeanscluster(starttime,endtime)
    starttime = starttime + Timeframe.windowsize
    endtime = endtime + Timeframe.windowsize

programendtime = datetime.datetime.now() # Record the system time After end of the Algorithm
print("\nAlgorithm End time:",programendtime)

# Calculate the difference between start and the end time
timeobj = programendtime - programstarttime

print ("Total time to run the Algorithm:", timeobj)
print("Average run time for each pool:",timeobj/numpool)

print ("\nTotal distance without ridesharing:",tnormaldist,"km")
print ("Total distance with ridesharing:",tridesharedist,"km")

print("\nNumber of pools:",numpool)

print ("\nAverage distance without ridesharing for eachpool:",tnormaldist/numpool,"km")
print ("Average distance with ridesharing for each pool",tridesharedist/numpool,"km")

print ("\nAverage number of trips Before RideSharing:",wolength/numpool)
print ("Average number of trips After RideSharing:",wlength/numpool)

