import os
os.environ["TESTING"] = "1"
import sys
import httpx

print("Step 1: importing app", flush=True)
from app.main import app

print("Step 2: creating httpx Client", flush=True)
client = httpx.Client(transport=httpx.ASGITransport(app=app), base_url="http://test")

print("Step 3: sending GET /api", flush=True)
r = client.get("/api")
print("Step 4: got response", r.status_code, r.json(), flush=True)
