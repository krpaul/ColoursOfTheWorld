import json

ranked = []
capitals = []

with open("heatmap/capitals.json") as c:
    capitals = json.loads(c.read())

with open("heatmap/sorted_ranked.txt") as f:
    ranked = f.readlines()
    for idx, line in enumerate(ranked):
        line = list(line.split(": "))
        line[1] = float(line[1])
        ranked[idx] = line

def find_coords_of_cap(country):
    for obj in capitals:
        if obj["CountryName"] == country:
            return (float(obj["CapitalLatitude"]), float(obj["CapitalLongitude"]))