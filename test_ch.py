import requests

url = "https://overpass.osm.ch/api/interpreter"
q = """[out:json][timeout:15];
(
  node["amenity"="hospital"](around:5000, 23.2599, 77.4126);
);
out body 5;"""

r = requests.post(url, data={'data': q}, timeout=15)
print("osm.ch status:", r.status_code)
print("osm.ch text:", r.text[:300])
