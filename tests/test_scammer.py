import requests
import json
import time

# Configuration
API_URL = "http://127.0.0.1:8000/chat"
HEADERS = {
    "x-api-key": "tinku_local_test_key",
    "Content-Type": "application/json"
}

# Simulated Scam Conversation
scenarios = [
    {
        "text": "Your SBI account is blocked. Update KYC immediately at http://sbi-secure-update.net",
        "description": "Initial Hook with Phishing Link"
    },
    {
        "text": "Send 1 Rs to verify your account. UPI ID: secure.pay@okaxis",
        "description": "Mule UPI Extraction"
    },
    {
        "text": "Provide your Aadhar and PAN details now or we will file an FIR.",
        "description": "High Pressure Tactic"
    }
]

def run_test():
    session_id = f"test-session-{int(time.time())}"
    history = []

    print(f"🚀 Starting Test for Session: {session_id}\n")

    for i, step in enumerate(scenarios):
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": step["text"],
                "timestamp": int(time.time() * 1000)
            },
            "conversationHistory": history
        }

        print(f"📡 Scammer [{i+1}]: {step['text']}")
        
        start_time = time.time()
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            reply = response.json().get("reply")
            print(f"🤖 Agent: {reply}")
            print(f"⏱️ Response Time: {elapsed:.2f}s (Includes jitter delay)")
            
            # Update history for next turn
            history.append({"sender": "scammer", "text": step["text"], "timestamp": payload["message"]["timestamp"]})
            history.append({"sender": "user", "text": reply, "timestamp": int(time.time() * 1000)})
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
        
        print("-" * 50)
        time.sleep(1)

if __name__ == "__main__":
    run_test()