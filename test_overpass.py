import requests
import json

mirrors = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
]

# Query using around filter (super fast in Overpass - spatial indexing!)
query = """
[out:json][timeout:15];
(
  node["amenity"="hospital"](around:10000, 23.2599, 77.4126);
  node["amenity"="restaurant"](around:10000, 23.2599, 77.4126);
);
out body 15;
"""

headers = {
    'User-Agent': 'BusinessListingsIntelligence/1.0 (academic research; contact: student@honeybeedigital.internal)'
}

for m in mirrors:
    print(f"Testing {m}...")
    try:
        r = requests.post(m, data={'data': query}, headers=headers, timeout=15)
        print("Status:", r.status_code)
        if r.status_code == 200:
            data = r.json()
            elements = data.get('elements', [])
            print(f"SUCCESS! Received {len(elements)} elements")
            for el in elements[:5]:
                tags = el.get('tags', {})
                print(" -", tags.get('name'), "|", tags.get('amenity'), "| phone:", tags.get('phone') or tags.get('contact:phone'))
            break
    except Exception as e:
        print("Failed:", e)
