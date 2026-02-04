# Agentic Honey-Pot for Scam Detection & Intelligence Extraction

AI-powered honeypot system designed to detect scam intent and autonomously engage scammers to extract actionable intelligence.

## 🚀 Features
- **Scam Detection Engine**: Multi-layered analysis of message content and tactics.
- **Autonomous AI Agent**: Handles multi-turn conversations with human-like personas and behavioral nuances (typos, jitter).
- **Intelligence Extraction**: Automatically harvests UPI IDs, bank accounts, phishing links, and phone numbers.
- **Strategic Reporting**: Mandated reporting to evaluation endpoints after sufficient engagement.
- **Secure**: Protected by API key authentication.

## 🛠️ API Documentation

### 1. Chat Endpoint
`POST /chat`

**Headers:**
- `x-api-key`: `YOUR_SECRET_API_KEY`
- `Content-Type`: `application/json`

**Payload:**
```json
{
  "sessionId": "wertyu-dfghj-ertyui",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today. Verify immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Why is my account being suspended? I am very worried."
}
```

## 🧠 Behavior & Strategy
The agent uses a phase-shifting strategy:
1. **Phase 1: Confusion**: Acts as a tech-illiterate victim to lower scammer's guard.
2. **Phase 2: Stalling**: Simulates technical issues (slow internet, battery low) to gain time.
3. **Phase 3: Trapping**: Actively offers payment or info to extract the scammer's "mule" details.

## 📊 Intelligence Extraction
Data is reported back once:
1. Scam intent is confirmed.
2. Sufficient engagement is reached (e.g., mule info harvested or turn limit reached).
3. The extracted intel is formatted into a structured final report.
