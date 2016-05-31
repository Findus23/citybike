#!/usr/bin/python3

import itertools
import os
import re
from pprint import pprint

import MySQLdb

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Findus",  # your password
                     db="citybike")  # name of the data base

cur = db.cursor()

cur.execute("SELECT lat, lon,ref FROM stationen ORDER BY ref DESC")
list = cur.fetchall()
i = 1
for way in itertools.combinations(list, 2):
    command = "routino-router --dir=/home/lukas/router/data" \
              " --lat1={}".format(way[0][0]) + \
              " --lon1={}".format(way[0][1]) + \
              " --lat2={}".format(way[1][0]) + \
              " --lon2={}".format(way[1][1]) + \
              " --quickest --transport=bicycle --output-text --output-gpx-track --quiet"
    success = os.system(command)
    if success == 0:
        os.rename("quickest-track.gpx", "file/" + str(i) + ".gpx")
        with open('quickest.txt') as f:
            lines = f.readlines()
            last = lines[-1]
            duration = re.findall("(\d+) min", last)[1]
            length = re.findall("(\d+\.\d+) km", last)[1]
            length = re.findall("(\d+\.\d+) km", last)[1]
        cur.execute("REPLACE INTO connections (id, start, goal, length, duration) VALUES (%s,%s,%s,%s,%s)",
                    (i, way[0][2], way[1][2], length, duration))
        db.commit()
    print(i)
    i += 1
db.commit()
