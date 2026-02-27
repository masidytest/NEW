# test_api.py
# Test script for the FastAPI backend

import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    print("=" * 70)
    print("TEST 1: Root endpoint")
    print("=" * 70)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_health():
    print("=" * 70)
    print("TEST 2: Health check")
    print("=" * 70)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_capabilities():
    print("=" * 70)
    print("TEST 3: List capabilities")
    print("=" * 70)
    response = requests.get(f"{BASE_URL}/capabilities")
    print(f"Status: {response.status_code}")
    caps = response.json()
    print(f"Total capabilities: {len(caps)}")
    for cap in caps:
        print(f"  • {cap['name']}: {cap['description']}")
        print(f"    Tags: {cap['tags']}")
    print()

def test_chat():
    print("=" * 70)
    print("TEST 4: Chat endpoint")
    print("=" * 70)
    
    messages = [
        "what is 5 + 3",
        "what time is it",
        "generate an image of a sunset"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"user_id": "test_user", "message": msg}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Agent: {data['reply'][:100]}...")
            print(f"Reasoning passes: {data['reasoning_passes']}")
    print()

def test_goals():
    print("=" * 70)
    print("TEST 5: Goals management")
    print("=" * 70)
    
    # Add a goal
    print("\nAdding goal...")
    response = requests.post(
        f"{BASE_URL}/goals",
        json={
            "user_id": "test_user",
            "description": "Learn about quantum computing",
            "priority": 2.5,
            "tags": ["learning", "quantum"]
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        goal = response.json()
        print(f"Created goal: {goal['goal_id']}")
        print(f"Description: {goal['description']}")
        print(f"Priority: {goal['priority']}")
    
    # List goals
    print("\nListing all goals...")
    response = requests.get(f"{BASE_URL}/goals")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        goals = response.json()
        print(f"Total goals: {len(goals)}")
        for g in goals:
            print(f"  • [{g['goal_id']}] {g['description']}")
            print(f"    Status: {g['status']}, Priority: {g['priority']}, Score: {g['score']:.2f}")
    print()

def test_autonomous():
    print("=" * 70)
    print("TEST 6: Autonomous cycle")
    print("=" * 70)
    
    response = requests.post(f"{BASE_URL}/autonomous")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data['status']}")
        if data['goal_id']:
            print(f"Goal: [{data['goal_id']}] {data['goal_description']}")
            print(f"Answer: {data['answer'][:200]}...")
        else:
            print(f"Message: {data['answer']}")
    print()

def test_gaps_and_plugins():
    print("=" * 70)
    print("TEST 7: Capability gaps and plugin proposals")
    print("=" * 70)
    
    # Get gaps
    print("\nCapability gaps:")
    response = requests.get(f"{BASE_URL}/gaps")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        gaps = response.json()
        if gaps:
            for gap in gaps:
                print(f"  • Missing: {gap['missing_tags']} (requested {gap['count']} times)")
        else:
            print("  No gaps detected yet")
    
    # Get plugin proposals
    print("\nPlugin proposals:")
    response = requests.get(f"{BASE_URL}/plugins")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        plugins = response.json()
        if plugins:
            for plugin in plugins:
                print(f"  • {plugin['name']}")
                print(f"    Tags: {plugin['tags']}")
                print(f"    Demand: {plugin['count']} requests")
        else:
            print("  No plugin proposals yet")
    print()

def run_all_tests():
    print("\n" + "=" * 70)
    print("FASTAPI BACKEND TEST SUITE")
    print("=" * 70)
    print("\nMake sure the server is running: uvicorn app:app --reload")
    print()
    
    try:
        test_root()
        test_health()
        test_capabilities()
        test_chat()
        test_goals()
        test_autonomous()
        test_gaps_and_plugins()
        
        print("=" * 70)
        print("ALL TESTS COMPLETED")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the server is running:")
        print("  uvicorn app:app --reload")
        print()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    run_all_tests()
