#!/usr/bin/python3

import subprocess
import json
from pprint import pprint
from config import database
import MySQLdb

db = MySQLdb.connect(database["host"],
                     database["user"],
                     database["passwd"],
                     database["db"])
cur = db.cursor()

cur.execute("SELECT ref FROM stationen ORDER BY ref DESC")
stationList = cur.fetchall()
geojsonFeatures = []
ways = set()
limit = 5
for station in stationList:
    sql = '''
SELECT
  id, start, goal
FROM connections
  LEFT JOIN stationen ON (start = ref OR goal = ref)
WHERE ref = {ref}
ORDER BY length
LIMIT {limit}
'''.format(ref=station[0], limit=limit)
    cur.execute(sql)
    nearest = cur.fetchall()
    for way in nearest:
        if not way[0] in ways:  # Wenn nicht schon hinzugefügt
            ways.add(way[0])
            print(str(way[0]))
            filename = str(way[0]) + ".gpx"
            geojsonString = subprocess.check_output(["togeojson", "file/" + filename]).decode('UTF-8')
            geojson = json.loads(geojsonString)
            feature = geojson["features"][0]
            del feature["properties"]["desc"], feature["properties"]["name"]  # Überreste von GPX entfernen
            feature["properties"]["nodes"] = [way[1], way[2]]
            feature["properties"]["id"] = way[0]
            geojsonFeatures.append(feature)
        else:
            print(str(way[0]) + ": Dup")

geojsonComplete = {
    "type": "FeatureCollection",
    "features": geojsonFeatures
}

with open('www/nearest.json', 'w') as outfile:
    json.dump(geojsonComplete, outfile)
