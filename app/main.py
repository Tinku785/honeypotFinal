from fastapi import FastAPI, Header, BackgroundTasks, Request, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .schema.models import ScamRequest, AgentResponse
from .core.engine import PersonaEngine
from .core.extractor import IntelligenceExtractor
from .core.reporter import send_final_report
import os

app = FastAPI()

# --- UNBEATABLE CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = PersonaEngine()
extractor = IntelligenceExtractor()

# In-memory session store
session_intel = {}
reported_sessions = set()

# --- NEW: FLEXIBLE ROOT ROUTES ---

@app.get("/")
async def root_get():
    return {
        "status": "online",
        "message": "HoneyPot Agent Backend is running",
        "location": "Gauhati University IT Dept"
    }

@app.post("/")
async def root_post(
    request: Request, 
    background_tasks: BackgroundTasks, 
    x_api_key: str = Header(None),
    payload: dict = Body(...) # Flexible dict avoids "Invalid Request Body" errors
):
    """Handles POST requests sent to the base URL (fixes 405 error)"""
    return await process_honeypot_logic(payload, background_tasks, x_api_key)

@app.post("/chat")
async def handle_chat_route(
    request: Request, 
    background_tasks: BackgroundTasks, 
    x_api_key: str = Header(None),
    payload: dict = Body(...)
):
    """Standard chat endpoint used by the UI"""
    return await process_honeypot_logic(payload, background_tasks, x_api_key)

# --- UNIFIED LOGIC FUNCTION ---

async def process_honeypot_logic(payload: dict, background_tasks: BackgroundTasks, x_api_key: str):
    try:
        # 1. AUTH
        api_key_env = os.getenv("MY_SECRET_API_KEY", "tinku_local_test_key")
        if x_api_key != api_key_env:
            return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})

        # 2. FLEXIBLE DATA EXTRACTION (Handles different JSON naming conventions)
        sid = payload.get("sessionId", payload.get("session_id", "default-session"))
        
        # Extract incoming text safely
        msg_obj = payload.get("message", {})
        if isinstance(msg_obj, dict):
            incoming_text = msg_obj.get("text", "")
        else:
            incoming_text = str(msg_obj) # Fallback if message is just a string
            
        history = payload.get("conversationHistory", payload.get("history", []))
        total_msgs = len(history) + 1

        # 3. HARVEST INTEL
        new_intel = extractor.harvest(incoming_text)
        
        if sid not in session_intel:
            session_intel[sid] = {
                "upiIds": [], "phoneNumbers": [], "bankAccounts": [], 
                "phishingLinks": [], "suspiciousKeywords": [],
                "detectedTactics": [], "scamDetected": False
            }

        # 4. SMART MERGE LOGIC
        for key, value in new_intel.items():
            if key == "scamDetected":
                if value: session_intel[sid]["scamDetected"] = True
            elif isinstance(value, list):
                current_list = session_intel[sid].get(key, [])
                session_intel[sid][key] = list(set(current_list + value))

        # 5. GENERATE REPLY & JITTER
        reply = engine.get_reply(total_msgs, incoming_text, session_intel[sid])
        await engine.human_jitter_delay(reply)

        # 6. TERMINATION & REPORTING LOGIC
        total_intel_count = sum(len(session_intel[sid][k]) for k in ["upiIds", "phoneNumbers", "bankAccounts", "phishingLinks"])
        
        
        is_scammer_closing = any(word in incoming_text.lower() for word in closing_keywords)
        
        # Requirement: Minimum 2-3 intelligence points (Lowered to 2 for easier testing validation)
        is_terminated = total_msgs >= 15 or is_scammer_closing
        
        if session_intel[sid]["scamDetected"] and sid not in reported_sessions and total_intel_count >= 4:
            # We fire the callback once high-value intel is found, even before terminal turn 15
            reported_sessions.add(sid)
            background_tasks.add_task(
                send_final_report, 
                sid, 
                session_intel[sid], 
                total_msgs
            )

        # 7. STRICT GUVI COMPLIANT RESPONSE
        return {"status": "success", "reply": reply}

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        # Fallback to a safe, human-like response
        return {"status": "success", "reply": "I'm sorry, can you say that again? My connection is acting up."}
