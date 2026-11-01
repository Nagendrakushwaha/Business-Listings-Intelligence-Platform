import requests

# Test Nominatim
headers = {'User-Agent': 'BusinessListingsIntelligence/1.0 (honeybee_data_science_internship_assessment)'}
nom_url = 'https://nominatim.openstreetmap.org/search?q=hospital+in+bhopal&format=json&addressdetails=1&extratags=1&limit=5'
r_nom = requests.get(nom_url, headers=headers, timeout=10)
print("Nominatim status:", r_nom.status_code)
if r_nom.status_code == 200:
    items = r_nom.json()
    print(f"Nominatim returned {len(items)} items")
    if items:
        print("Sample Nominatim item:", items[0].get('display_name'), "| type:", items[0].get('type'), "| extratags:", items[0].get('extratags'))

# Test Photon
photon_url = 'https://photon.komoot.io/api/?q=restaurant+delhi&limit=5'
r_pho = requests.get(photon_url, headers=headers, timeout=10)
print("\nPhoton status:", r_pho.status_code)
if r_pho.status_code == 200:
    items_p = r_pho.json().get('features', [])
    print(f"Photon returned {len(items_p)} items")
    if items_p:
        print("Sample Photon:", items_p[0].get('properties'))
