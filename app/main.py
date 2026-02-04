from fastapi import FastAPI, Header, BackgroundTasks, Request, HTTPException
from .schema.models import ScamRequest, AgentResponse
from .core.engine import PersonaEngine
from .core.extractor import IntelligenceExtractor
from .core.reporter import send_final_report
import os

from fastapi import FastAPI, Header, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware # This is the correct path

app = FastAPI()

# --- UNBEATABLE CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (essential for local UI testing)
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, OPTIONS, GET, etc.
    allow_headers=["*"],  # Allows x-api-key, Content-Type, etc.
)
# -------------------------------------


engine = PersonaEngine()
extractor = IntelligenceExtractor()












# In-memory session store (In a Hero system, use Redis)
session_intel = {}
reported_sessions = set()

@app.post("/chat", response_model=AgentResponse)
async def handle_chat(request: ScamRequest, background_tasks: BackgroundTasks, x_api_key: str = Header(None)):
    try:
        # 1. AUTH
        api_key_env = os.getenv("MY_SECRET_API_KEY", "tinku_local_test_key")
        if x_api_key != api_key_env:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        sid = request.sessionId
        incoming_text = request.message.text
        total_msgs = len(request.conversationHistory) + 1

        # 2. HARVEST INTEL
        new_intel = extractor.harvest(incoming_text)
        
        # Update local session memory
        if sid not in session_intel:
            session_intel[sid] = {
                "upiIds": [], 
                "phoneNumbers": [], 
                "bankAccounts": [], 
                "phishingLinks": [], 
                "suspiciousKeywords": [],
                "detectedTactics": [],
                "scamDetected": False
            }
        
        # 3. SMART MERGE LOGIC
        for key, value in new_intel.items():
            if key == "scamDetected":
                if value: session_intel[sid]["scamDetected"] = True
            elif isinstance(value, list):
                current_list = session_intel[sid].get(key, [])
                combined = list(set(current_list + value))
                session_intel[sid][key] = combined

        # 4. GENERATE REPLY
        reply = engine.get_reply(total_msgs, incoming_text, session_intel[sid])
        
        # 5. SIMULATE HUMAN JITTER
        await engine.human_jitter_delay(reply)

        # 6. STRATEGIC CALLBACK (Section 12)
        is_scam = session_intel[sid]["scamDetected"]
        has_tech_intel = any([
            session_intel[sid]["upiIds"],
            session_intel[sid]["bankAccounts"],
            session_intel[sid]["phoneNumbers"],
            session_intel[sid]["phishingLinks"]
        ])
        total_intel_count = (
            len(session_intel[sid]["upiIds"]) + 
            len(session_intel[sid]["phoneNumbers"]) + 
            len(session_intel[sid]["bankAccounts"]) + 
            len(session_intel[sid]["phishingLinks"])
        )
        
        # 7. TERMINATION & REPORTING LOGIC (Section 12)
        # Requirement: Minimum 3 intelligence points AND session must be "terminated/completed"
        # We define "terminated" as:
        # A) Reaching a maximum turn limit (e.g., 15 turns)
        # B) The scammer using closing/end keywords (e.g., "bye", "finished", "thank you")
        
        closing_keywords = ["bye", "done", "finished", "complete", "thanks", "thank you"]
        is_scammer_closing = any(word in incoming_text.lower() for word in closing_keywords)
        
        is_terminated = total_msgs >= 15 or is_scammer_closing
        
        if is_scam and sid not in reported_sessions and total_intel_count >= 3 and is_terminated:
            reported_sessions.add(sid)
            print(f"DEBUG: SESSION_TERMINATED for {sid}. Intel Count: {total_intel_count}, Msgs: {total_msgs}")
            background_tasks.add_task(
                send_final_report, 
                sid, 
                session_intel[sid], 
                total_msgs + 1
            )

        return AgentResponse(reply=reply)

    except Exception as e:
        print(f"CRITICAL ERROR in handle_chat: {str(e)}")
        # Fallback to a safe, human-like error response
        return AgentResponse(reply="I'm sorry, my phone just did something strange. Can you say that again?")
