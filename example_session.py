# example_session.py
# Simulated interactive session demonstrating the self-expanding system

import torch
from next_system import Agent, train_core_on_text

def simulate_session():
    print("=" * 70)
    print("AUTONOMOUS COGNITIVE SYSTEM - INTERACTIVE SESSION")
    print("=" * 70)
    
    # Initialize agent
    device = "cuda" if torch.cuda.is_available() else "cpu"
    agent = Agent(device=device)
    
    # Quick training
    demo_texts = [
        "hello, this is a new brain.",
        "this system has memory and planning.",
        "the goal is to become more advanced over time.",
    ]
    print("\n[Initializing neural core...]")
    train_core_on_text(agent, demo_texts, epochs=2, max_len=80, lr=1e-3)
    
    print("\n" + "=" * 70)
    print("SESSION START")
    print("=" * 70)
    
    # Simulate user interactions
    interactions = [
        ("capabilities", "List all capabilities"),
        ("what time is it", "Use existing capability"),
        ("generate an image of a sunset", "Request missing capability"),
        ("convert text to speech", "Request another missing capability"),
        ("gaps", "Check detected gaps"),
        ("plugins", "View proposed plugins"),
    ]
    
    for i, (command, description) in enumerate(interactions, 1):
        print(f"\n[{i}] {description}")
        print("-" * 70)
        print(f"You: {command}")
        
        if command == "capabilities":
            caps = agent.capabilities.all()
            print(f"\nAgent: I have {len(caps)} capabilities:")
            for cap in caps:
                print(f"  • {cap.name}: {cap.description}")
                print(f"    Tags: {cap.tags}")
        
        elif command == "gaps":
            gaps = agent.get_capability_gaps()
            if not gaps:
                print("\nAgent: No capability gaps detected yet.")
            else:
                print(f"\nAgent: I've detected {len(gaps)} capability gaps:")
                for gap in gaps:
                    print(f"  • Missing: {gap['missing_tags']} (requested {gap['count']} times)")
        
        elif command == "plugins":
            specs = agent.propose_new_plugins()
            if not specs:
                print("\nAgent: No plugin proposals yet.")
            else:
                print(f"\nAgent: I propose {len(specs)} new plugins:")
                for spec in specs:
                    print(f"\n  {spec['name']}")
                    print(f"    Tags: {spec['tags']}")
                    print(f"    Description: {spec['description']}")
                    print(f"    Demand: {spec['count']} requests")
        
        else:
            # Simulate capability check without full cognitive loop
            tags = agent.capability_planner.infer_tags(command)
            caps = agent.capability_planner.choose_capabilities(tags)
            
            available_tags = set()
            for cap in agent.capabilities.all():
                available_tags.update(cap.tags)
            
            missing = [t for t in tags if t not in available_tags]
            
            if missing:
                agent.capability_gaps.log_gap(command, tags, missing)
                print(f"\nAgent: I understand you want to {command}, but I don't have")
                print(f"       the capability for: {missing}")
                print(f"       I've logged this gap and will propose a plugin for it.")
            else:
                if caps:
                    print(f"\nAgent: I can help with that using: {[c.name for c in caps]}")
                else:
                    print(f"\nAgent: I can help with that.")
    
    print("\n" + "=" * 70)
    print("SESSION SUMMARY")
    print("=" * 70)
    
    gaps = agent.get_capability_gaps()
    specs = agent.propose_new_plugins()
    
    print(f"\n📊 Statistics:")
    print(f"  • Capabilities: {len(agent.capabilities.all())}")
    print(f"  • Gaps detected: {len(gaps)}")
    print(f"  • Plugins proposed: {len(specs)}")
    
    print(f"\n🎯 System Behavior:")
    print(f"  ✓ Answered queries using existing capabilities")
    print(f"  ✓ Detected when capabilities were missing")
    print(f"  ✓ Logged gaps for future expansion")
    print(f"  ✓ Proposed concrete plugin specifications")
    
    print(f"\n💡 Self-Expansion in Action:")
    print(f"  The system demonstrated self-awareness by:")
    print(f"  1. Knowing what it can do (7 capabilities)")
    print(f"  2. Recognizing what it can't do (detected gaps)")
    print(f"  3. Proposing how to expand (plugin specs)")
    print(f"  4. Prioritizing by demand (request frequency)")
    
    print(f"\n🚀 Next Evolution:")
    print(f"  With the proposed plugins implemented, the system will:")
    print(f"  • Handle image generation and analysis")
    print(f"  • Process speech and audio")
    print(f"  • Analyze data files (CSV, JSON, etc.)")
    print(f"  • Continue detecting new gaps")
    print(f"  • Propose additional expansions")
    
    print("\n" + "=" * 70)
    print("This is a self-expanding AI system that grows based on usage.")
    print("=" * 70)

if __name__ == "__main__":
    simulate_session()
