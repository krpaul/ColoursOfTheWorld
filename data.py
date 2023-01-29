import json
import math

ranked = []
capitals = []
lats = []
lngs = []

with open("heatmap/capitals.json") as c:
    capitals = json.loads(c.read())

with open("heatmap/sorted_ranked.txt") as f:
    ranked = f.readlines()
    for idx, line in enumerate(ranked):
        line = list(line.split(": "))
        line[1] = float(line[1])
        ranked[idx] = line

with open("heatmap/land_coords.json") as l:
    list_ = json.loads(l.read())
    lats = list_[0::2]
    lngs = list_[1::2]

def create_radius(lat, lng, magnitude, radius):
    points_lat = []
    points_lng = []
    magnitudes = []

    magnitude /= 3

    for r in range(1, int(radius)):
        for theta in range(0, 360, 20):
            s = r * math.sin(math.radians(theta))
            c = r * math.cos(math.radians(theta))

            points_lat.append(lat + s)
            points_lng.append(lng + c)
            magnitudes.append(r/radius * magnitude)

    z = list(zip(lats, lngs))

    i = 0
    for lt, lg in zip(points_lat, points_lng):
        if (round(lt), round(lg)) not in z:# and (math.floor(lt), math.floor(lg)) not in z and (math.ceil(lt), math.ceil(lg)) not in z:
            del points_lat[i]
            del points_lng[i]
        
        i += 1

    return zip(points_lat + [lat], points_lng + [lng], list(reversed(magnitudes)) + [magnitude*2])

def find_coords_of_cap(country):
    for obj in capitals:
        if obj["CountryName"] == country:
            return (float(obj["CapitalLatitude"]), float(obj["CapitalLongitude"]))