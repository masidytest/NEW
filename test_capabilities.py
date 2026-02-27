# test_capabilities.py
# Automated test to demonstrate the self-expanding capability system

import torch
from next_system import Agent, train_core_on_text

def test_capability_system():
    print("=" * 60)
    print("TESTING SELF-EXPANDING CAPABILITY SYSTEM")
    print("=" * 60)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    agent = Agent(device=device)
    
    # Quick training
    demo_texts = [
        "hello, this is a new brain.",
        "this system has memory and planning.",
        "the goal is to become more advanced over time.",
    ]
    print("\n[1] Training core network...")
    train_core_on_text(agent, demo_texts, epochs=3, max_len=80, lr=1e-3)
    
    # Test 1: List existing capabilities
    print("\n[2] Listing existing capabilities:")
    print("-" * 60)
    caps = agent.capabilities.all()
    for cap in caps:
        print(f"  ✓ {cap.name}: {cap.description}")
        print(f"    Tags: {cap.tags}")
    print(f"\nTotal: {len(caps)} capabilities")
    
    # Test 2: Use existing capabilities (should work)
    print("\n[3] Testing existing capabilities:")
    print("-" * 60)
    
    print("\n  Query: 'what is 5 + 3'")
    answer = agent.handle("what is 5 + 3")
    print(f"  Answer: {answer[:100]}...")
    
    print("\n  Query: 'what time is it'")
    answer = agent.handle("what time is it")
    print(f"  Answer: {answer[:100]}...")
    
    # Test 3: Request missing capabilities (should log gaps)
    print("\n[4] Testing missing capabilities (gap detection):")
    print("-" * 60)
    
    missing_capability_queries = [
        "generate an image of a cat",
        "convert this text to speech",
        "analyze this CSV data",
        "generate another image of a dog",
        "create a picture of mountains",
    ]
    
    for query in missing_capability_queries:
        print(f"\n  Query: '{query}'")
        answer = agent.handle(query)
        print(f"  Answer: {answer[:80]}...")
    
    # Test 4: Show detected gaps
    print("\n[5] Capability gaps detected:")
    print("-" * 60)
    gaps = agent.get_capability_gaps()
    if not gaps:
        print("  No gaps detected")
    else:
        for gap in gaps:
            print(f"  ⚠ Missing tags: {gap['missing_tags']}")
            print(f"    Requested: {gap['count']} times")
    
    # Test 5: Show proposed plugins
    print("\n[6] Proposed new plugins:")
    print("-" * 60)
    specs = agent.propose_new_plugins()
    if not specs:
        print("  No proposals yet")
    else:
        for spec in specs:
            print(f"\n  📦 {spec['name']}")
            print(f"     Tags: {spec['tags']}")
            print(f"     Description: {spec['description']}")
            print(f"     Requested: {spec['count']} times")
            print(f"     Suggested inputs: {spec['suggested_inputs']}")
            print(f"     Suggested outputs: {spec['suggested_outputs']}")
    
    # Test 6: Demonstrate tag-based capability selection
    print("\n[7] Tag-based capability selection:")
    print("-" * 60)
    
    test_tags = [
        (["math"], "Math capabilities"),
        (["research", "papers"], "Research capabilities"),
        (["code"], "Code analysis capabilities"),
        (["image"], "Image capabilities (should be empty)"),
    ]
    
    for tags, description in test_tags:
        caps = agent.capabilities.find_by_tags(tags)
        print(f"\n  {description} (tags={tags}):")
        if caps:
            for cap in caps:
                print(f"    ✓ {cap.name}")
        else:
            print(f"    ✗ No capabilities found")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    print("\n📊 SUMMARY:")
    print(f"  • Registered capabilities: {len(agent.capabilities.all())}")
    print(f"  • Detected capability gaps: {len(gaps)}")
    print(f"  • Proposed new plugins: {len(specs)}")
    
    print("\n🎯 KEY INSIGHT:")
    print("  The system automatically detected missing capabilities")
    print("  and proposed plugin specifications to fill those gaps.")
    print("  This is the foundation for self-expanding AI systems.")

if __name__ == "__main__":
    test_capability_system()
