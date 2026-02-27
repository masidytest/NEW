# quick_test.py
# Quick demonstration of self-expanding capability system

import torch
from next_system import Agent

def quick_test():
    print("=" * 70)
    print("SELF-EXPANDING CAPABILITY SYSTEM - QUICK DEMO")
    print("=" * 70)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    agent = Agent(device=device)
    
    # Test 1: Show existing capabilities
    print("\n[1] EXISTING CAPABILITIES:")
    print("-" * 70)
    caps = agent.capabilities.all()
    for cap in caps:
        print(f"  ✓ {cap.name:<20} Tags: {cap.tags}")
    print(f"\n  Total: {len(caps)} capabilities registered")
    
    # Test 2: Simulate capability gap detection
    print("\n[2] SIMULATING USER REQUESTS (Gap Detection):")
    print("-" * 70)
    
    test_queries = [
        ("what is 5 + 3", ["math"]),
        ("what time is it", ["time"]),
        ("generate an image of a cat", ["image"]),
        ("convert text to speech", ["speech"]),
        ("analyze this CSV file", ["data"]),
        ("create a picture of mountains", ["image"]),
        ("read this audio file", ["speech"]),
    ]
    
    for query, expected_tags in test_queries:
        # Infer tags from query
        tags = agent.capability_planner.infer_tags(query)
        
        # Find matching capabilities
        caps = agent.capability_planner.choose_capabilities(tags)
        
        # Check for gaps
        available_tags = set()
        for cap in agent.capabilities.all():
            available_tags.update(cap.tags)
        
        missing = [t for t in tags if t not in available_tags]
        
        status = "✓ COVERED" if not missing else "⚠ GAP DETECTED"
        print(f"\n  Query: '{query}'")
        print(f"  Inferred tags: {tags}")
        print(f"  Status: {status}")
        
        if caps:
            print(f"  Matched capabilities: {[c.name for c in caps]}")
        
        if missing:
            print(f"  Missing tags: {missing}")
            agent.capability_gaps.log_gap(query, tags, missing)
    
    # Test 3: Show capability gaps summary
    print("\n[3] CAPABILITY GAPS SUMMARY:")
    print("-" * 70)
    gaps = agent.get_capability_gaps()
    if not gaps:
        print("  No gaps detected")
    else:
        for gap in gaps:
            tags_str = str(gap['missing_tags'])
            print(f"  ⚠ Missing: {tags_str:<30} Requested: {gap['count']} times")
    
    # Test 4: Show proposed plugins
    print("\n[4] PROPOSED NEW PLUGINS:")
    print("-" * 70)
    specs = agent.propose_new_plugins()
    if not specs:
        print("  No proposals yet")
    else:
        for i, spec in enumerate(specs, 1):
            print(f"\n  Plugin #{i}: {spec['name']}")
            print(f"    Tags: {spec['tags']}")
            print(f"    Description: {spec['description']}")
            print(f"    Demand: {spec['count']} requests")
    
    # Test 5: Demonstrate tag-based lookup
    print("\n[5] TAG-BASED CAPABILITY LOOKUP:")
    print("-" * 70)
    
    test_lookups = [
        ["math"],
        ["research"],
        ["code"],
        ["image"],  # should be empty
        ["speech"], # should be empty
    ]
    
    for tags in test_lookups:
        caps = agent.capabilities.find_by_tags(tags)
        tags_str = str(tags)
        if caps:
            cap_names = [c.name for c in caps]
            print(f"  Tags {tags_str:<20} → {cap_names}")
        else:
            print(f"  Tags {tags_str:<20} → [NO CAPABILITIES FOUND]")
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    
    print("\n📊 FINAL STATISTICS:")
    print(f"  • Registered capabilities: {len(agent.capabilities.all())}")
    print(f"  • Unique capability gaps: {len(gaps)}")
    print(f"  • Proposed plugins: {len(specs)}")
    
    print("\n🎯 KEY FEATURES DEMONSTRATED:")
    print("  1. ✓ Capability registry with semantic tags")
    print("  2. ✓ Automatic tag inference from user queries")
    print("  3. ✓ Gap detection when capabilities are missing")
    print("  4. ✓ Plugin specification generation")
    print("  5. ✓ Tag-based capability discovery")
    
    print("\n💡 SELF-EXPANSION PATH:")
    print("  Current: 7 capabilities (math, time, research, code)")
    print("  Detected needs: image, speech, data processing")
    print("  Next step: Implement proposed plugins")
    print("  Future: System drafts plugin code automatically")
    
    print("\n🚀 This is a self-expanding AI system that:")
    print("  • Knows what it can do")
    print("  • Knows what it can't do")
    print("  • Proposes how to expand itself")
    print("  • Grows based on actual usage patterns")

if __name__ == "__main__":
    quick_test()
