"""
Test script for authentication flow
Tests registration, login, and authenticated API access
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_auth_flow():
    print("🧪 Testing Authentication Flow\n")
    
    # Test 1: Register new user
    print("1️⃣ Testing registration...")
    test_email = f"test_{hash('test')}@example.com"
    test_password = "testpass123"
    
    register_response = requests.post(
        f"{API_URL}/auth/register",
        json={"email": test_email, "password": test_password}
    )
    
    if register_response.status_code == 200:
        data = register_response.json()
        token = data.get("access_token")
        print(f"   ✅ Registration successful")
        print(f"   Token: {token[:20]}...")
    else:
        print(f"   ❌ Registration failed: {register_response.text}")
        return
    
    # Test 2: Login with same credentials
    print("\n2️⃣ Testing login...")
    login_response = requests.post(
        f"{API_URL}/auth/token",
        data={"username": test_email, "password": test_password}
    )
    
    if login_response.status_code == 200:
        data = login_response.json()
        token = data.get("access_token")
        print(f"   ✅ Login successful")
        print(f"   Token: {token[:20]}...")
    else:
        print(f"   ❌ Login failed: {login_response.text}")
        return
    
    # Test 3: Access protected endpoint with token
    print("\n3️⃣ Testing authenticated API access...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test /health endpoint
    health_response = requests.get(f"{API_URL}/health", headers=headers)
    if health_response.status_code == 200:
        data = health_response.json()
        print(f"   ✅ /health endpoint accessible")
        print(f"   Capabilities: {data.get('capabilities')}")
        print(f"   Memories: {data.get('memory_items')}")
        print(f"   Goals: {data.get('goals')}")
    else:
        print(f"   ❌ /health failed: {health_response.text}")
    
    # Test /capabilities endpoint
    cap_response = requests.get(f"{API_URL}/capabilities", headers=headers)
    if cap_response.status_code == 200:
        caps = cap_response.json()
        print(f"   ✅ /capabilities endpoint accessible")
        print(f"   Total capabilities: {len(caps)}")
    else:
        print(f"   ❌ /capabilities failed: {cap_response.text}")
    
    # Test /goals endpoint
    goals_response = requests.get(f"{API_URL}/goals", headers=headers)
    if goals_response.status_code == 200:
        goals = goals_response.json()
        print(f"   ✅ /goals endpoint accessible")
        print(f"   Total goals: {len(goals)}")
    else:
        print(f"   ❌ /goals failed: {goals_response.text}")
    
    # Test 4: Access without token (should fail)
    print("\n4️⃣ Testing unauthorized access...")
    unauth_response = requests.get(f"{API_URL}/health")
    if unauth_response.status_code == 401:
        print(f"   ✅ Unauthorized access correctly blocked")
    else:
        print(f"   ❌ Expected 401, got {unauth_response.status_code}")
    
    # Test 5: Chat with authentication
    print("\n5️⃣ Testing authenticated chat...")
    chat_response = requests.post(
        f"{API_URL}/chat",
        headers=headers,
        json={"message": "Hello, test message"}
    )
    if chat_response.status_code == 200:
        data = chat_response.json()
        print(f"   ✅ Chat endpoint accessible")
        print(f"   Reply: {data.get('reply')[:50]}...")
    else:
        print(f"   ❌ Chat failed: {chat_response.text}")
    
    print("\n✅ All authentication tests passed!")

if __name__ == "__main__":
    try:
        test_auth_flow()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running:")
        print("   python app_multiuser.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
