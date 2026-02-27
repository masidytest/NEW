"""
Test script for the unified server (serve_static.py)
Run this before deploying to Railway to ensure everything works
"""
import subprocess
import time
import requests
import sys

def test_unified_server():
    print("🧪 Testing Unified Server (serve_static.py)")
    print("=" * 50)
    print()
    
    # Start server
    print("1️⃣ Starting server...")
    process = subprocess.Popen(
        ["python", "serve_static.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    print("   Waiting for server to start...")
    time.sleep(5)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: API root
        print("\n2️⃣ Testing API root...")
        response = requests.get(f"{base_url}/api")
        if response.status_code == 200:
            print("   ✅ API root accessible")
            data = response.json()
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
        else:
            print(f"   ❌ API root failed: {response.status_code}")
        
        # Test 2: Static homepage (login page)
        print("\n3️⃣ Testing static homepage...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200 and "login" in response.text.lower():
            print("   ✅ Homepage (login page) accessible")
        else:
            print(f"   ❌ Homepage failed: {response.status_code}")
        
        # Test 3: Chat page
        print("\n4️⃣ Testing chat page...")
        response = requests.get(f"{base_url}/chat.html")
        if response.status_code == 200 and "chat" in response.text.lower():
            print("   ✅ Chat page accessible")
        else:
            print(f"   ❌ Chat page failed: {response.status_code}")
        
        # Test 4: Goals page
        print("\n5️⃣ Testing goals page...")
        response = requests.get(f"{base_url}/goals.html")
        if response.status_code == 200 and "goals" in response.text.lower():
            print("   ✅ Goals page accessible")
        else:
            print(f"   ❌ Goals page failed: {response.status_code}")
        
        # Test 5: Capabilities page
        print("\n6️⃣ Testing capabilities page...")
        response = requests.get(f"{base_url}/capabilities.html")
        if response.status_code == 200 and "capabilities" in response.text.lower():
            print("   ✅ Capabilities page accessible")
        else:
            print(f"   ❌ Capabilities page failed: {response.status_code}")
        
        # Test 6: Register endpoint
        print("\n7️⃣ Testing registration endpoint...")
        test_email = f"test_{int(time.time())}@example.com"
        response = requests.post(
            f"{base_url}/auth/register",
            json={"email": test_email, "password": "testpass123"}
        )
        if response.status_code == 200:
            print("   ✅ Registration endpoint works")
            token = response.json().get("access_token")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
        
        # Test 7: Capabilities endpoint
        print("\n8️⃣ Testing capabilities endpoint...")
        response = requests.get(f"{base_url}/capabilities")
        if response.status_code == 200:
            caps = response.json()
            print(f"   ✅ Capabilities endpoint works")
            print(f"   Total capabilities: {len(caps)}")
        else:
            print(f"   ❌ Capabilities failed: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print()
        print("🚀 Ready to deploy to Railway!")
        print()
        print("Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Deploy to Railway'")
        print("3. git push")
        print("4. Go to https://railway.app and deploy")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server")
        print("   Make sure the server started successfully")
        print("   Check for errors in the terminal")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    finally:
        # Stop server
        print("\n9️⃣ Stopping server...")
        process.terminate()
        process.wait()
        print("   ✅ Server stopped")

if __name__ == "__main__":
    test_unified_server()
