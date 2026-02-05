import re  # <--- THIS IS THE MISSING PIECE
import json
import os



class IntelligenceExtractor:
    def __init__(self):
        # 1. Technical Patterns (Infrastructure)
        self.patterns = {
            # Sharp UPI Regex
            "upiIds": r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9]+',
            
            # Generic Phone Regex: Matches sequences of digits, +, -, and spaces
            "phoneNumbers": r'\+?[\d\s\-]{10,20}', 
            
            "bankAccounts": r'\b\d{11,18}\b',
            "phishingLinks": r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        }
        
        # 2. Linguistic Intelligence (Tactics)
        self.tactic_map = {
            "Fear & Accusation": [
                "blocked", "suspended", "police", "arrest", "legal", "illegal", "fraud", 
                "court", "complaint", "fir", "jail", "criminal", "investigation", "penalty", 
                "fine", "frozen", "npa", "defaulter", "cbi", "cyber cell", "summons", 
                "warrant", "action today", "permanent block", "blacklisted", "suspicious activity"
            ],
            "Urgency & Pressure": [
                "urgent", "immediately", "today", "now", "9:30pm", "10pm", "fast", 
                "seconds", "last warning", "final notice", "hurry", "quick", "dont wait", 
                "before tonight", "9pm", "within 10 minutes", "instantly", "limited time", 
                "midnight", "expire", "ending", "verify immediately", "verify now", "act now"
            ],
            "Authority Impersonation": [
                "sbi", "hdfc", "apdcl", "bank", "manager", "official", "bijulee bhawan", 
                "head office", "yono", "icici", "axis", "pnb", "rbi", "government", 
                "electricity board", "power house", "department", "sharma ji", "baruah sir", 
                "staff", "branch", "helpline", "support desk", "verification officer", "customer care"
            ],
            "Social Engineering (Technical)": [
                "otp", "cvv", "kyc", "verify", "link", "anydesk", "teamviewer", "rustdesk", 
                "code", "pin", "upin", "vpa", "pan card", "aadhaar", "biometric", "update", 
                "re-verification", "scratch card", "rewards", "coupon", "claim", "qr code", 
                "scan now", "authentication", "approval", "sms link", "click here"
            ],
            "Incentive & Job Traps": [
                "telegram", "work from home", "wfh", "part time", "salary", "bonus", 
                "daily income", "amazon merchant", "youtube like", "google review", 
                "rating task", "registration fee", "security deposit", "payout", 
                "merchant task", "level 1", "vip member", "whatsapp group", "instagram job",
                "hiring", "earn daily", "extra money", "profit share", "lucky winner", "prize"
            ]
        }

    def harvest(self, text: str):
        text_lower = text.lower()
        
        # 1. Extract hard technical data
        harvested = {}
        for key, pattern in self.patterns.items():
            found = re.findall(pattern, text)
            
            # Cleanup for phone numbers (Requirement: digits between 10 and 12)
            if key == "phoneNumbers":
                cleaned = []
                for f in found:
                    # Keep only digits to count them
                    digits = "".join(filter(str.isdigit, f))
                    # Requirement: >= 10 and <= 12 digits
                    if 10 <= len(digits) <= 12:
                        # Append the cleaned digit string
                        cleaned.append(digits)
                found = cleaned
                
            harvested[key] = list(set(found))
        
        # 2. Extract tactics and actual suspicious keywords
        found_keywords = []
        detected_tactics = []
        for tactic, keywords in self.tactic_map.items():
            tactic_matched = False
            for word in keywords:
                if word in text_lower:
                    found_keywords.append(word)
                    tactic_matched = True
            if tactic_matched:
                detected_tactics.append(tactic)
        
        harvested["suspiciousKeywords"] = list(set(found_keywords))
        harvested["detectedTactics"] = list(set(detected_tactics))
        
        # Calculate Scam Confidence
        # Higher threshold for detection to avoid false positives
        has_tech_intel = any(len(v) > 0 for k, v in harvested.items() if k not in ["suspiciousKeywords", "detectedTactics"])
        has_tactic_keywords = len(found_keywords) >= 1
        
        harvested["scamDetected"] = has_tech_intel or has_tactic_keywords
        return harvested
