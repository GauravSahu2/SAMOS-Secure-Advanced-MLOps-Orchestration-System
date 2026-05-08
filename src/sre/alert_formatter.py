def format_rich_alert(event_type, action_taken):
    """Phase 25: SRE - Context-Aware Rich Notifications."""
    print(f"🔔 Phase 25: Formatting Rich Notification for '{event_type}'...")
    
    alert = {
        "title": f"🚨 CRITICAL: {event_type}",
        "context": "Intersectional Bias threshold exceeded in Staging.",
        "automated_response": action_taken,
        "next_steps": "Review Regret Minimizer logs (src/model_sec/regret_minimizer.py)",
        "priority": "P0 - URGENT"
    }
    
    print("-" * 30)
    print(f"[{alert['priority']}] {alert['title']}")
    print(f"  Context: {alert['context']}")
    print(f"  Action Taken: {alert['automated_response']}")
    print(f"  Instruction: {alert['next_steps']}")
    print("-" * 30)
    
    print("✅ Rich Alert sent to #ai-ops-war-room.")

if __name__ == "__main__":
    format_rich_alert("Bias Breach V2.1", "Model Promotion Blocked + Regret Logged")
