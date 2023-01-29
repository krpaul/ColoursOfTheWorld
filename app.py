from flask import Flask, render_template, jsonify, request
from data import ranked, capitals, find_coords_of_cap, create_radius
from charity.grab import grab_charities
from time import time

import geopy.distance

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get-heat")
def heat():
    data = list(ranked)
    data2 = []

    for d in data:
        coords = find_coords_of_cap(d[0])
        if coords == None: continue
        coords = list(coords)
        
        magnitude = (abs(d[1]) ** 0.66)
        radius = magnitude * 15

        magnitude *= 1.2

        coords.append(magnitude)

        x = create_radius(*coords, radius)
        for a in x:
            data2.extend(a)

    return jsonify(data2)

last_req = 0;
@app.route("/get-charities")
def chars():
    if not time() - last_req > 5:
        return jsonify({})

    min_d = 99999999
    cap = None
    for c in capitals:
        dist = geopy.distance.geodesic((request.args["lat"], request.args["lng"]), (float(c["CapitalLatitude"]), float(c["CapitalLongitude"]))).km
        if dist < min_d:
            min_d = dist
            cap = c

    return jsonify(grab_charities(cap["CountryName"]))