from flask import Flask, render_template, jsonify
from data import ranked, capitals, find_coords_of_cap, create_radius

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
