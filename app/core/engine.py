import random
import asyncio
from .behavior import BehaviorSynthesizer

class PersonaEngine:
    def __init__(self):
        self.synthesizer = BehaviorSynthesizer()
        self.strategies = {
            "CONFUSED": [
                "I am getting a notification saying 'Security Alert'. Is that you?",
                "Wait, my grandson usually helps me with this. Which button is 'Continue'?",
                "The screen is blurry, let me find my glasses.",
                "Is this the official bank number? My phone says 'Potential Scam' but I don't believe it.",
                "Wait, I am clicking but nothing is happening. Should I click harder?",
                "Is the 'Continue' button the blue one or the green one?",
                "I'm sorry, I am a bit slow with these new smartphones.",
                "Does the bank always call at this time? I was just about to have tea.",
                "Are you calling from the branch near the park?",
                "I see a lot of numbers here, which one do you need exactly?",
                "I think my battery is at 2%. Let me find the charger first.",
                "Wait, my cat just jumped on the table. One second.",
                "I am ready to help, but can you explain what happened to my account?",
                "Should I be worried? My heart is beating very fast.",
                "The screen just went dark. Oh, it's back. Scared me!",
                "Are you the same person who called last month?",
                "Wait, I need to find my reading glasses. Hold on.",
                "Is this about that lottery I won?"
            ],
            "STALL": [
                "My internet is very slow today, the circle is just spinning.",
                "Wait, my phone is ringing from another number. Is that your colleague?",
                "I am typing the numbers but it keeps saying 'Incorrect'. Let me try again.",
                "One second, my wife is asking who is on the phone.",
                "The OTP is not coming. Should I click 'Resend' or wait?",
                "I am putting in the password. Wait, I forgot if the 'S' was capital.",
                "My signal is dropping. Can you hear me? Hello?",
                "I am looking for the card in my wallet. I have too many receipts in here.",
                "Wait, the phone updated itself and restarted! Please stay on the line.",
                "I am trying to find a pen to write this down. Hold on.",
                "I think I typed the wrong UPI PIN. Let me try the other one.",
                "Wait, someone is at the door. Let me see who it is.",
                "The keyboard on my phone is acting weird. It's typing double letters.",
                "I am trying to find my checkbook. It should be in this drawer.",
                "Wait, I need to clear some space on my phone, it says 'Storage Full'.",
                "I'm clicking 'Allow' but it keeps asking again. What do I do?",
                "It says 'Connection Timeout'. Should I refresh the page?",
                "Wait, I accidentally turned on the flashlight. How do I turn it off?",
                "Is the code 4 digits or 6 digits? I am confused."
            ],
            "TRAP": [
                "Can I just send it via UPI? My card is not working. What is your ID?",
                "If I pay now, will my account be unblocked immediately?",
                "I have another account in HDFC. Should we link that one too?",
                "Do you need my Aadhaar number as well? I have it right here.",
                "What is the name of your supervisor? I want to tell them how helpful you are.",
                "If I give you my UPI ID, can you just 'Request' the money from me?",
                "Can I talk to your manager? I want to make sure this is the right way.",
                "I have some money in my digital wallet too. Can we use that?",
                "Can you give me your personal number in case the call drops?",
                "I have a screenshot of the payment. Where should I send it?",
                "Is there a discount if I pay the full amount now?",
                "Can I use my wife's UPI ID for this? Her name is Anjali.",
                "Can you verify my last transaction? It was for 500 rupees at the grocery store.",
                "Is this the same department that handles home loans?",
                "I am ready to transfer. What is the account holder's name?",
                "Can I pay via QR code? Can you send me one?",
                "Will this update my mobile number in the records too?",
                "I have 50,000 in my account. Will it all be safe after this?",
                "Can you call me back in 5 minutes from a landline?",
                "I am ready to click Pay. Just tell me the ID one more time."
            ]
        }

    def get_reply(self, total_msgs: int, text: str, intel: dict = None):
        text_lower = text.lower()
        tactics = intel.get("detectedTactics", []) if intel else []
        
        # 1. Higher-Priority Reactive Logic (Specific Tactics)
        if "Fear & Accusation" in tactics:
            return self.synthesizer.apply_typo(random.choice([
                "Oh no, I don't want to go to jail! Please help me, I have a family.",
                "Is this about that legal notice? I am very worried about my bank account being frozen.",
                "I promise I didn't do anything wrong! What do I need to do to stop the police from coming?"
            ]))
        
        if "Incentive & Job Traps" in tactics:
            return self.synthesizer.apply_typo(random.choice([
                "I really need the extra money. Is it really just liking YouTube videos for salary?",
                "I joined the Telegram group but I am not sure how to start the tasks. Can you show me?",
                "Will I get my bonus today? I am ready to work hard."
            ]))
            
        if "Authority Impersonation" in tactics:
            return self.synthesizer.apply_typo(random.choice([
                "I didn't know the head office would call me personally! Thank you for helping an old man.",
                "Yes sir, I see you are from the bank. I was just about to go to the branch.",
                "Is this the verification department? I have my Aadhaar card ready."
            ]))

        # 2. Key-phrase Reactive Logic (Functional Responses)
        if any(word in text_lower for word in ["otp", "code", "pin", "password"]):
            return self.synthesizer.apply_typo(random.choice([
                "I am looking at my messages, but there are so many. Is it a 6-digit one?",
                "Wait, my phone says 'Do not share'. Is it safe to give you this code?",
                "The screen just refreshed and the code disappeared. Can you send it one more time?"
            ]))
            
        if any(word in text_lower for word in ["app", "download", "install", "anydesk", "support", "rustdesk"]):
            return self.synthesizer.apply_typo("I searched for the app but there are so many options. Does it have the blue logo or the red one? I don't want to download a virus.")
            
        if any(word in text_lower for word in ["pay", "money", "transfer", "upi", "bank"]):
            if total_msgs < 6:
                return self.synthesizer.apply_typo("I want to pay to fix this, but my UPI is showing 'Limit Exceeded'. Can I send it to your personal ID instead?")
            else:
                return self.synthesizer.apply_typo(random.choice(self.strategies["TRAP"]))

        # 3. Dynamic Frustration/Correction Handling
        if any(word in text_lower for word in ["wrong", "mistake", "error", "listen", "no", "not", "hello"]):
            return self.synthesizer.apply_typo("I am so sorry! I think I clicked the wrong button. I am so clumsy with these things. Can you explain what I should do again?")

        # 4. Phase-based Fallback (If no specific match found)
        if total_msgs < 4:
            reply = random.choice(self.strategies["CONFUSED"])
        elif total_msgs < 8:
            reply = random.choice(self.strategies["STALL"])
        else:
            reply = random.choice(self.strategies["TRAP"])

        return self.synthesizer.apply_typo(reply)

    async def human_jitter_delay(self, reply: str):
        """Simulates human 'Thinking + Typing' time with randomness."""
        delay = self.synthesizer.calculate_human_delay(reply)
        await asyncio.sleep(min(delay, 5.0)) # Cap at 5s to avoid API timeouts
