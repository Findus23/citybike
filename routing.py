#!/usr/bin/python3

import itertools
import os
import subprocess
import xml.dom.minidom

import MySQLdb
from tqdm import tqdm

from config import database
from gpxlen import getTrackLength

db = MySQLdb.connect(database["host"],
                     database["user"],
                     database["passwd"],
                     database["db"])

cursor = db.cursor()

cursor.execute("SELECT lat, lon,ref FROM stationen ORDER BY ref DESC")  # Liste der Stationen
stations = cursor.fetchall()
routeID = 1
totalCombinations = 14641  # 212 über 2
pbar = tqdm(total=totalCombinations)

for way in itertools.product(stations, repeat=2):
    command = [
        "routino-router",
        "--dir=/home/lukas/routino/data",
        "--lat1={}".format(way[0][0]),
        "--lon1={}".format(way[0][1]),
        "--lat2={}".format(way[1][0]),
        "--lon2={}".format(way[1][1]),
        "--quickest",
        "--transport=bicycle",
        "--output-gpx-track",
        "--quiet"
    ]
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        os.rename("quickest-track.gpx", "file/" + str(routeID) + ".gpx")  # nach file/2.gpx verschieben
        dom = xml.dom.minidom.parse("file/" + str(routeID) + ".gpx")
        gpxNode = dom.firstChild
        length = round(getTrackLength(gpxNode.getElementsByTagName("trk")[0]), 0)  # Länge aus gpx auslesen

        cursor.execute("REPLACE INTO connections (id, start, goal, length) VALUES (%s,%s,%s,%s)",
                       (routeID, way[0][2], way[1][2], length))  # in db eintragen
    except subprocess.CalledProcessError as exception:
        print()  # Neue Zeile
        print("Fehler zwischen Station " + str(way[0][2]) + " und " + str(way[1][2]))
        print(exception.output.decode())
    pbar.update(1)
    # stdout.write("\r{:.4f}".format(routeID / totalCombinations * 100))  # Prozentanzeige
    routeID += 1
pbar.close()
db.commit()
