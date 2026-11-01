import requests

instances = [
    'https://overpass-api.de/api/interpreter',
    'https://lz4.overpass-api.de/api/interpreter',
    'https://z.overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.openstreetmap.ru/cgi/interpreter',
    'https://overpass.osm.ch/api/interpreter',
    'https://overpass.private.coffee/api/interpreter'
]

# Simple bounding box query for Delhi (small area)
q = """[out:json][timeout:10];
node["amenity"="restaurant"](28.61,77.20,28.65,77.25);
out 5;"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HoneybeeAssessment/1.0'
}

for inst in instances:
    print(f"Testing {inst}...")
    try:
        resp = requests.post(inst, data={'data': q}, headers=headers, timeout=8)
        print(f"-> {inst} returned {resp.status_code}, len={len(resp.text)}")
        if resp.status_code == 200:
            data = resp.json()
            print("FOUND ELEMENTS:", len(data.get('elements', [])))
            break
    except Exception as e:
        print(f"-> {inst} failed: {type(e).__name__}")
