import requests
import json
import logging

# Set up a logger to help you see errors in Render logs without a crash
logger = logging.getLogger(__name__)

def send_final_report(session_id: str, intel: dict, total_msgs: int):
    url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    # --- NO CHANGES TO YOUR LOGIC BELOW ---
    tactics = intel.get("detectedTactics", [])
    tactic_str = f"The scammer employed {', '.join(tactics)} tactics." if tactics else "The scammer used generic fraudulent persuasion."
    
    intel_parts = []
    if intel.get('upiIds'): intel_parts.append(f"{len(intel['upiIds'])} UPI IDs ({', '.join(intel['upiIds'])})")
    if intel.get('phoneNumbers'): intel_parts.append(f"{len(intel['phoneNumbers'])} Phone Numbers")
    if intel.get('bankAccounts'): intel_parts.append(f"{len(intel['bankAccounts'])} potential Bank Accounts")
    if intel.get('phishingLinks'): intel_parts.append(f"{len(intel['phishingLinks'])} Phishing Links")
    
    intel_str = f" Extracted high-value intelligence: {', '.join(intel_parts)}." if intel_parts else " No specific payment or contact details were extracted yet."
    behavior_str = f" The AI Agent maintained a believable tech-illiterate persona over {total_msgs} messages, successfully stalling the scammer and extracting actionable data."
    notes = f"{tactic_str}{intel_str}{behavior_str}"

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total_msgs,
        "extractedIntelligence": {
            "bankAccounts": intel.get("bankAccounts", []),
            "upiIds": intel.get("upiIds", []),
            "phishingLinks": intel.get("phishingLinks", []),
            "phoneNumbers": intel.get("phoneNumbers", []),
            "suspiciousKeywords": intel.get("suspiciousKeywords", [])
        },
        "agentNotes": notes
    }
    # --- END OF YOUR LOGIC ---

    # IMPROVED: Using a Session with proper error trapping for Render stability
    try:
        with requests.Session() as session:
            # Increased timeout to 10s to account for potential slow GUVI API response
            response = session.post(url, json=payload, timeout=10)
            
            # This will raise an error for 4xx or 5xx responses so we can log them
            response.raise_for_status() 
            
            print(f"✅ REPORT SENT SUCCESSFULLY: {session_id}")
            
    except requests.exceptions.Timeout:
        print(f"⚠️ REPORT TIMEOUT: GUVI API took too long for session {session_id}")
    except requests.exceptions.RequestException as e:
        # This catches connection errors, DNS issues, etc.
        print(f"❌ REPORT NETWORK ERROR: {e}")
    except Exception as e:
        # Final catch-all to prevent the entire FastAPI process from shutting down
        print(f"⚠️ UNEXPECTED REPORTER ERROR: {e}")
