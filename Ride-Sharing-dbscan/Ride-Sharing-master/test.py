import mysql.connector
from mysql.connector import errorcode
from math import radians,sin,cos,asin,sqrt
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import Timeframe

def db_connect():
    try:
        cnn = mysql.connector.connect(
            user='root',
            password='123456',
            host='localhost',
            port=3306,
            database='trip_data')
        return cnn
        # print("it works")
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_CHANGE_USER_ERROR:
            print("somethind os wrong with username and password")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("database doesn't exist")
        else:
            print(e)

def selecteachpool(cursor, starttime, endtime):
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

    return coord_list, passenger_count

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
    db = DBSCAN(eps=1, min_samples=3, metric=lambda a, b:haversine(a, b))
    coord_list_source_np = np.array(coord_list_source)
    db.fit(coord_list_source_np)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = coord_list_source_np[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = coord_list_source_np[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()

starttime = Timeframe.starttime
endtime = Timeframe.endtime
cnn = db_connect()
cursor = cnn.cursor()
coord_list, passenger_count = selecteachpool(cursor, starttime, endtime)
dbscancluster(coord_list)