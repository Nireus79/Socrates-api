#!/usr/bin/env python
"""Run API and test endpoints."""
import subprocess
import time
import requests
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Start API with output capture
print("[INFO] Starting API...")
api = subprocess.Popen(
    [sys.executable, '-m', 'socrates_api'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Let it start
time.sleep(8)

try:
    # Check if auth routes are available by listing app routes
    from socrates_api.main import app
    auth_routes = [r.path for r in app.routes if '/auth' in r.path]
    print("[DEBUG] Auth routes in app object: %d" % len(auth_routes))

    # Try to hit the registration endpoint
    print("\n[TEST] POST /auth/register")
    resp = requests.post('http://localhost:8000/auth/register',
                        json={'username': 'test789', 'password': 'Test789!@#', 'email': 'test789@test.com'},
                        timeout=5)
    print("[RESULT] Status: %d" % resp.status_code)
    print("[RESULT] Response: %s" % resp.text[:100])

finally:
    # Stop API
    print("\n[INFO] Stopping API...")
    api.terminate()

    # Print startup output
    try:
        stdout, stderr = api.communicate(timeout=2)
        if "Auth routes" in stdout or "auth_router" in stdout:
            print("[DEBUG] Auth-related output from startup:")
            for line in stdout.split('\n'):
                if 'auth' in line.lower():
                    print("  " + line)
    except:
        pass
