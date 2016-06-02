#!/usr/bin/python3

import itertools
import os
import xml.dom.minidom
from pprint import pprint
import MySQLdb

from config import database
from gpxlen import getTrackLength

db = MySQLdb.connect(database["host"],
                     database["user"],
                     database["passwd"],
                     database["db"])

cursor = db.cursor()

cursor.execute("SELECT lat, lon,ref FROM stationen ORDER BY ref DESC")
stations = cursor.fetchall()
id = 1
for way in itertools.combinations(stations, 2):
    command = "routino-router --dir=/home/lukas/router/data" \
              " --lat1={}".format(way[0][0]) + \
              " --lon1={}".format(way[0][1]) + \
              " --lat2={}".format(way[1][0]) + \
              " --lon2={}".format(way[1][1]) + \
              " --quickest --transport=bicycle --output-gpx-track --quiet"
    success = os.system(command)
    if success == 0:
        os.rename("quickest-track.gpx", "file/" + str(id) + ".gpx")
        dom = xml.dom.minidom.parse("file/" + str(id) + ".gpx")
        gpxNode = dom.firstChild
        length = round(getTrackLength(gpxNode.getElementsByTagName("trk")[0]), 0)

        cursor.execute("REPLACE INTO connections (id, start, goal, length) VALUES (%s,%s,%s,%s)",
                       (id, way[0][2], way[1][2], length))
    else:
        print("   " + str(way[0][2]) + "   " + str(way[1][2]))
    print(id)
    id += 1
db.commit()
