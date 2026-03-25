#!/usr/bin/env python
"""Test that the API can start with proper environment setup."""
import os
import sys

# Print current directory
print(f"Current directory: {os.getcwd()}")

# Import the package (which calls load_dotenv)
import socrates_api
print("[OK] socrates_api package imported")

# Check if JWT_SECRET_KEY is now loaded
jwt_key = os.getenv("JWT_SECRET_KEY")
print(f"JWT_SECRET_KEY loaded: {bool(jwt_key)}")
if jwt_key:
    print(f"JWT_SECRET_KEY value: {jwt_key[:30]}...")

# Try to import the main app
try:
    from socrates_api.main import app
    print("[OK] FastAPI app initialized successfully")
    print(f"[OK] App title: {app.title}")
    print(f"[OK] App version: {app.version}")

    # Check routes
    routes = [route.path for route in app.routes]
    auth_routes = [r for r in routes if '/auth' in r]
    print(f"[OK] Total routes: {len(routes)}")
    print(f"[OK] Auth routes found: {len(auth_routes)}")
    if auth_routes:
        print(f"     Sample auth routes: {auth_routes[:3]}")

except Exception as e:
    print(f"[FAIL] Error initializing app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[PASS] API startup test successful!")
