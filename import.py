#!/usr/bin/python3
import json
import sys
from pprint import pprint
from config import database

import MySQLdb

try:

    db = MySQLdb.connect(database["host"],
                         database["user"],
                         database["passwd"],
                         database["db"])

    cur = db.cursor()

    with open('stationLayer.json') as data_file:
        data = json.load(data_file)
    for station in data["elements"]:
        if station["type"] == "node":
            tags=station["tags"]
            cur.execute("INSERT INTO stationen (ref, lon, lat, name) VALUES (%s,%s,%s,%s)", (tags["ref"], station["lon"], station["lat"], tags["name"]))
            print(tags["name"])
    print("Commiting")
    db.commit()

    db.close()

except MySQLdb.Error as e:

    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)
