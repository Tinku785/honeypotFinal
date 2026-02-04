import requests
import json

def send_final_report(session_id: str, intel: dict, total_msgs: int):
    url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    # 1. Tactics Summary
    tactics = intel.get("detectedTactics", [])
    tactic_str = f"The scammer employed {', '.join(tactics)} tactics." if tactics else "The scammer used generic fraudulent persuasion."
    
    # 2. Intelligence Summary
    intel_parts = []
    if intel.get('upiIds'): intel_parts.append(f"{len(intel['upiIds'])} UPI IDs ({', '.join(intel['upiIds'])})")
    if intel.get('phoneNumbers'): intel_parts.append(f"{len(intel['phoneNumbers'])} Phone Numbers")
    if intel.get('bankAccounts'): intel_parts.append(f"{len(intel['bankAccounts'])} potential Bank Accounts")
    if intel.get('phishingLinks'): intel_parts.append(f"{len(intel['phishingLinks'])} Phishing Links")
    
    intel_str = f" Extracted high-value intelligence: {', '.join(intel_parts)}." if intel_parts else " No specific payment or contact details were extracted yet."
    
    # 3. Behavioral Summary
    behavior_str = f" The AI Agent maintained a believable tech-illiterate persona over {total_msgs} messages, successfully stalling the scammer and extracting actionable data."
    
    # Final combined notes
    notes = f"{tactic_str}{intel_str}{behavior_str}"

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total_msgs,
        "extractedIntelligence": {
            "bankAccounts": intel["bankAccounts"],
            "upiIds": intel["upiIds"],
            "phishingLinks": intel["phishingLinks"],
            "phoneNumbers": intel["phoneNumbers"],
            "suspiciousKeywords": intel["suspiciousKeywords"]
        },
        "agentNotes": notes
    }

    try:
        requests.post(url, json=payload, timeout=5)
        print(f"REPORT SENT: {session_id}")
    except Exception as e:
        print(f"Callback Log ERROR: {e}")

        