#!/usr/bin/python3
import json
import sys
from pprint import pprint

import requests

from config import database

import MySQLdb

try:

    db = MySQLdb.connect(database["host"],
                         database["user"],
                         database["passwd"],
                         database["db"])

    cur = db.cursor()

    payload = {
        "data": (
            '[out:json][timeout:25];'
            'area(3600109166)->.searchArea;'
            'node["amenity"="bicycle_rental"]["network"="Citybike Wien"](area.searchArea);'
            'out body;>;out skel qt;'
        )

    }
    print("Overpass Abfrage")
    r = requests.get('https://overpass-api.de/api/interpreter', params=payload)
    data = r.json()
    print("erfolgreich")
    i = 0
    for station in data["elements"]:
        if station["type"] == "node":
            tags = station["tags"]
            cur.execute("REPLACE INTO stationen (ref, lon, lat, name) VALUES (%s,%s,%s,%s)",
                        (tags["ref"], station["lon"], station["lat"], tags["name"]))
            i += 1
    db.commit()
    print("%s Stationen importiert" % i)
    db.close()

except MySQLdb.Error as e:

    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)
