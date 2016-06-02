#!/usr/bin/python3

import subprocess
import json
from pprint import pprint

import MySQLdb

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Findus",  # your password
                     db="citybike")  # name of the data base

cur = db.cursor()

cur.execute("SELECT ref FROM stationen ORDER BY ref DESC")
list = cur.fetchall()
geojsonFeatures = []
ways = set()
for station in list:
    sql = '''
SELECT
  id, start, goal
FROM connections
  LEFT JOIN stationen ON (start = ref OR goal = ref)
WHERE ref = {ref}
ORDER BY length
LIMIT 3
'''.format(ref=station[0])
    cur.execute(sql)
    nearest = cur.fetchall()
    for way in nearest:
        if not way[0] in ways:
            ways.add(way[0])
            print(str(way[0]))
            filename = str(way[0]) + ".gpx"
            geojsonString = subprocess.check_output(["togeojson", "file/" + filename]).decode('UTF-8')
            geojson = json.loads(str(geojsonString))
            feature = geojson["features"][0]
            del feature["properties"]["desc"], feature["properties"]["name"]  # Überreste von GPX entfernen
            feature["properties"]["nodes"] = [way[1], way[2]]
            geojsonFeatures.append(feature)
        else:
            print(str(way[0]) + ": Dup")

geojsonComplete = {}
geojsonComplete["type"] = "FeatureCollection"
geojsonComplete["features"] = geojsonFeatures

with open('test.json', 'w') as outfile:
    json.dump(geojsonComplete, outfile, indent=4)
