from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Message(BaseModel):
    sender: str  # "scammer" or "user"
    text: str
    timestamp: int  # Epoch time in ms

class Metadata(BaseModel):
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata] = None

class AgentResponse(BaseModel):
    status: str = "success"
    reply: str

class Intelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []
    agentNotes: Optional[str] = ""