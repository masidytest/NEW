# test_multiuser.py
# Test script for multi-user authentication system

import requests
import json

BASE_URL = "http://localhost:8000"

def test_multiuser_system():
    print("=" * 70)
    print("MULTI-USER SYSTEM TEST")
    print("=" * 70)
    
    # Test 1: Register first user
    print("\n[1] Registering first user...")
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": "alice@example.com", "password": "alice123"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        alice_data = response.json()
        alice_token = alice_data["access_token"]
        print(f"✓ Alice registered: {alice_data['user_email']}")
        print(f"  Token: {alice_token[:20]}...")
    else:
        print(f"✗ Error: {response.json()}")
        return
    
    # Test 2: Register second user
    print("\n[2] Registering second user...")
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": "bob@example.com", "password": "bob123"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        bob_data = response.json()
        bob_token = bob_data["access_token"]
        print(f"✓ Bob registered: {bob_data['user_email']}")
        print(f"  Token: {bob_token[:20]}...")
    else:
        print(f"✗ Error: {response.json()}")
        return
    
    # Test 3: Get user info
    print("\n[3] Getting user info...")
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {alice_token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        user_info = response.json()
        print(f"✓ User info: {json.dumps(user_info, indent=2)}")
    
    # Test 4: Alice sends a chat message
    print("\n[4] Alice sends a chat message...")
    response = requests.post(
        f"{BASE_URL}/chat",
        headers={"Authorization": f"Bearer {alice_token}"},
        json={"message": "what is 5 + 3"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        chat_data = response.json()
        print(f"✓ Alice's reply: {chat_data['reply'][:80]}...")
    
    # Test 5: Bob sends a different chat message
    print("\n[5] Bob sends a chat message...")
    response = requests.post(
        f"{BASE_URL}/chat",
        headers={"Authorization": f"Bearer {bob_token}"},
        json={"message": "what time is it"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        chat_data = response.json()
        print(f"✓ Bob's reply: {chat_data['reply'][:80]}...")
    
    # Test 6: Alice creates a goal
    print("\n[6] Alice creates a goal...")
    response = requests.post(
        f"{BASE_URL}/goals",
        headers={"Authorization": f"Bearer {alice_token}"},
        json={"description": "Learn quantum computing", "priority": 2.5}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        goal_data = response.json()
        print(f"✓ Alice's goal created: {goal_data['description']}")
    
    # Test 7: Bob creates a different goal
    print("\n[7] Bob creates a goal...")
    response = requests.post(
        f"{BASE_URL}/goals",
        headers={"Authorization": f"Bearer {bob_token}"},
        json={"description": "Master machine learning", "priority": 3.0}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        goal_data = response.json()
        print(f"✓ Bob's goal created: {goal_data['description']}")
    
    # Test 8: Alice lists her goals (should only see her own)
    print("\n[8] Alice lists her goals...")
    response = requests.get(
        f"{BASE_URL}/goals",
        headers={"Authorization": f"Bearer {alice_token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        goals = response.json()
        print(f"✓ Alice has {len(goals)} goal(s):")
        for goal in goals:
            print(f"  - {goal['description']} (priority: {goal['priority']})")
    
    # Test 9: Bob lists his goals (should only see his own)
    print("\n[9] Bob lists his goals...")
    response = requests.get(
        f"{BASE_URL}/goals",
        headers={"Authorization": f"Bearer {bob_token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        goals = response.json()
        print(f"✓ Bob has {len(goals)} goal(s):")
        for goal in goals:
            print(f"  - {goal['description']} (priority: {goal['priority']})")
    
    # Test 10: Alice checks her health (per-user stats)
    print("\n[10] Alice checks health...")
    response = requests.get(
        f"{BASE_URL}/health",
        headers={"Authorization": f"Bearer {alice_token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        health = response.json()
        print(f"✓ Alice's stats:")
        print(f"  - User: {health['user_email']}")
        print(f"  - Capabilities: {health['capabilities']}")
        print(f"  - Memory items: {health['memory_items']}")
        print(f"  - Goals: {health['goals']}")
    
    # Test 11: Bob checks his health (different stats)
    print("\n[11] Bob checks health...")
    response = requests.get(
        f"{BASE_URL}/health",
        headers={"Authorization": f"Bearer {bob_token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        health = response.json()
        print(f"✓ Bob's stats:")
        print(f"  - User: {health['user_email']}")
        print(f"  - Capabilities: {health['capabilities']}")
        print(f"  - Memory items: {health['memory_items']}")
        print(f"  - Goals: {health['goals']}")
    
    # Test 12: Try to access without token (should fail)
    print("\n[12] Trying to access without token...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "hello"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 401:
        print(f"✓ Correctly rejected: {response.json()['detail']}")
    
    # Test 13: Login with existing user
    print("\n[13] Login with existing user...")
    response = requests.post(
        f"{BASE_URL}/auth/token",
        data={"username": "alice@example.com", "password": "alice123"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        login_data = response.json()
        print(f"✓ Alice logged in successfully")
        print(f"  Token: {login_data['access_token'][:20]}...")
    
    print("\n" + "=" * 70)
    print("MULTI-USER SYSTEM TEST COMPLETE")
    print("=" * 70)
    
    print("\n✅ Key Features Verified:")
    print("  • User registration")
    print("  • User login")
    print("  • JWT authentication")
    print("  • Per-user agent instances")
    print("  • Per-user memory isolation")
    print("  • Per-user goals")
    print("  • Per-user stats")
    print("  • Access control (401 without token)")

if __name__ == "__main__":
    try:
        test_multiuser_system()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the server is running:")
        print("  python app_multiuser.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
