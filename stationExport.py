#!/usr/bin/python3
import json
from pprint import pprint

import MySQLdb

from config import database

db = MySQLdb.connect(database["host"],
                     database["user"],
                     database["passwd"],
                     database["db"])

cursor = db.cursor()

cursor.execute("SELECT lon, lat,ref,name FROM stationen ORDER BY ref DESC")
stations = cursor.fetchall()

features = []
for station in stations:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                station[0],
                station[1]
            ]
        },
        "properties": {
            "name": station[3],
            "ref": station[2]
        }
    }
    features.append(feature)
geojsonComplete = {
    "type": "FeatureCollection",
    "features": features
}
# print(json.dumps(geojsonComplete, indent=4))
with open('stations.json', 'w') as outfile:
    json.dump(geojsonComplete, outfile, indent=4)
