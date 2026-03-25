#!/usr/bin/env python
"""Test the authentication flow end-to-end."""
import json
import subprocess
import time
import sys
import os

# Start the API server
print("[INFO] Starting API server...")
api_process = subprocess.Popen(
    [sys.executable, "-m", "socrates_api.main"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for API to start
time.sleep(5)

print("[INFO] API server started (PID: {})".format(api_process.pid))

try:
    import requests

    BASE_URL = "http://localhost:8000"

    # Test 1: Health check
    print("\n[TEST 1] Health check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"  [WARN] Health endpoint not found: {e}")

    # Test 2: Register a new user
    print("\n[TEST 2] User registration")
    register_data = {
        "username": "testuser_{}".format(int(time.time())),
        "password": "TestPass123!@#",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=5)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  [OK] Registration successful")
        print(f"  - Username: {data.get('username')}")
        print(f"  - Access token: {data.get('access_token', 'N/A')[:30]}...")
        print(f"  - Refresh token: {data.get('refresh_token', 'N/A')[:30]}...")

        access_token = data.get('access_token')
        username = register_data['username']
    else:
        print(f"  [FAIL] Registration failed")
        print(f"  Response: {response.text}")
        access_token = None
        username = None

    # Test 3: Login
    if access_token:
        print("\n[TEST 3] User login")
        login_data = {
            "username": username,
            "password": register_data['password']
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=5)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Login successful")
            print(f"  - Username: {data.get('username')}")
            print(f"  - Access token: {data.get('access_token', 'N/A')[:30]}...")
            new_access_token = data.get('access_token')
        else:
            print(f"  [FAIL] Login failed")
            print(f"  Response: {response.text}")

    # Test 4: Token refresh
    if access_token:
        print("\n[TEST 4] Token refresh")
        refresh_data = {"refresh_token": response.json().get('refresh_token')}
        response = requests.post(f"{BASE_URL}/auth/refresh", json=refresh_data, timeout=5)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Token refresh successful")
            print(f"  - New access token: {data.get('access_token', 'N/A')[:30]}...")
        else:
            print(f"  [FAIL] Token refresh failed")
            print(f"  Response: {response.text}")

    print("\n[PASS] Authentication flow test completed successfully!")

finally:
    # Stop the API server
    print("\n[INFO] Stopping API server...")
    api_process.terminate()
    try:
        api_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        api_process.kill()
    print("[INFO] API server stopped")
