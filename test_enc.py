import requests

s = requests.Session()
s.headers.clear()
s.headers['User-Agent'] = 'Mozilla/5.0'
s.headers['Accept'] = '*/*'
r = s.get('https://overpass-api.de/api/status')
print("Without extra headers:", r.status_code)

# Test french overpass
try:
    r_fr = requests.get('https://overpass.openstreetmap.fr/api/status', timeout=5)
    print("FR status:", r_fr.status_code)
except Exception as e:
    print("FR err:", e)
