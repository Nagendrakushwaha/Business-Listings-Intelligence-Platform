import requests
r = requests.post('https://overpass-api.de/api/interpreter', data='[out:json];node(1);out;')
print("Raw status:", r.status_code)
print("Raw headers:", dict(r.headers))
print("Raw text:", r.text)
