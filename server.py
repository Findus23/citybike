#!/usr/bin/env python3
import json
import subprocess

import MySQLdb
from flask import Flask
from flask import abort
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import request
from flask import send_file
from flask import send_from_directory
from flask import url_for
from flask_cache import Cache

from config import database
import top

db = MySQLdb.connect(database["host"],
                     database["user"],
                     database["passwd"],
                     database["db"])
cur = db.cursor()

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=False
)


@app.route('/api/connection/', methods=["GET"])
def getConnection():
    if not request.args \
            or 'from' not in request.args or 'to' not in request.args \
            or not request.args["from"].isdigit() or not request.args["to"].isdigit():
        abort(400)
    cur.execute("SELECT id FROM connections WHERE start = %s AND goal = %s", [request.args["from"], request.args["to"]])
    result = cur.fetchone()
    if not result:
        abort(404)
    return redirect(url_for("get_connection", connection_id=int(result[0])))


@app.route('/api/connection/<int:connection_id>', methods=['GET'])
def get_connection(connection_id):
    try:
        print("HIT")
        with open("file/" + str(connection_id) + ".json") as f:
            data = json.load(f)
            return jsonify(data)

    except EnvironmentError:
        print("MISS")
        cur.execute("SELECT  start, goal, length FROM connections WHERE id=%s", [connection_id])
        result = cur.fetchone()
        geojson = []
        try:
            geojsonstring = subprocess.check_output(["togeojson", "file/" + str(connection_id) + ".gpx"]).decode(
                'UTF-8')
            geojson = json.loads(geojsonstring)
            feature = geojson["features"][0]
            del feature["properties"]["desc"], feature["properties"]["name"]  # Überreste von GPX entfernen
            feature["properties"]["wayLength"] = result[2]
            feature["properties"]["nodes"] = [result[0], result[1]]
            feature["properties"]["id"] = connection_id
            geojson["features"][0] = feature
            with open("file/" + str(connection_id) + ".json", 'w') as outfile:
                json.dump(geojson, outfile, indent=4)
        except subprocess.CalledProcessError:
            abort(404)
        return jsonify(geojson)


def make_cache_key(*args, **kwargs): return request.url


@app.route('/api/top/', methods=["GET"])
@cache.cached(timeout=50, key_prefix=make_cache_key)
def get_top():
    if not request.args \
            or 'type' not in request.args \
            or 'pageSize' not in request.args \
            or 'pageNumber' not in request.args:
        print(request.args)
        abort(400)
    return jsonify(top.helloworld(cur, request.args))


@app.route('/')
def send_main_html():
    return send_file('www/map.html')


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('www', path)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': str(error)}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': str(error)}), 400)


if __name__ == "__main__":
    app.run(debug=True)
