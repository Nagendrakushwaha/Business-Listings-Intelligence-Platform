import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Test GET request
url = 'https://overpass-api.de/api/interpreter?data=[out:json];node(1);out;'
r = requests.get(url, headers=headers, timeout=10)
print("GET status:", r.status_code, r.text[:200])

# Test POST with Content-Type application/x-www-form-urlencoded
r_post = requests.post(
    'https://overpass-api.de/api/interpreter',
    data={'data': '[out:json];node(1);out;'},
    headers=headers,
    timeout=10
)
print("POST status:", r_post.status_code, r_post.text[:200])
