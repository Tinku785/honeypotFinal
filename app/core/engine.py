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
                "Please don't call the police, I’ve never even had a parking ticket!",
                "I'm shaking so much I can barely hold my phone, give me a second.",
                "My heart is racing, is there any way to settle this without going to jail?",
                "I have a family to look after, I can’t afford to have my bank account blocked.",
                "Is this because of that message I got yesterday about the electricity bill?",
                "I promise I didn't do anything wrong, I'm just a simple person.",
                "Wait, let me put on my glasses, I can’t see the screen clearly.",
                "My phone keeps lagging, I think it’s because it’s an old model.",
                "Can you hold on? Someone is at the door and I don’t want them to hear this.",
                "I am trying to follow you, but everything is moving so fast.",
                "Can you give me your official department number? My bank says I need to verify who I’m talking to.",
                "Is there a manager's mobile number I can reach if we get disconnected?",
                "My signal is weak, can you call me from a different number? This one shows as 'Unknown'.",
                "I want to save your number as 'Bank Support,' what is the best number to call back?",
                "Can I have your WhatsApp number? It’s easier for me to send you the details there.",
                "My son wants to talk to you to make sure this is real, what number should he call?",
                "The line is very crackly, do you have a toll-free number I can try?",
                "I'm writing this down—tell me the number for your fraud department again?",
                "Is this your direct office line or just a general number?",
                "If I lose my internet, how do I reach you on your personal extension?",
                "I am on the payment screen now, can you type the UPI ID exactly as it appears?",
                "The app says 'Recipient Not Found,' are you sure this is the right UPI address?",
                "I don’t use UPI, can I just get your bank account number and IFSC code instead?",
                "Which bank is this account with? My app is asking for the bank name.",
                "I have the cash here, can I deposit it into your account at a local branch?",
                "Is the UPI ID registered under your name or the department's name?",
                "I tried to add you as a beneficiary, but it’s asking for a branch address.",
                "Can you send me a screenshot of the QR code? My scanner isn't working.",
                "The limit for UPI is 10,000, do you have another account for the rest of the amount?",
                "Wait, is this a business account or a personal one? The app is giving me a warning.",
                "The link you sent didn't open, can you send the full website URL again?",
                "My browser says this site is 'Unsafe,' is there an official government link I should use?",
                "Can you email me the link? I find it easier to open things on my laptop.",
                "I'm on the SBI website but I don't see the 'Block' button, where is the link for that?",
                "Is there a portal link where I can upload my Aadhaar card safely?",
                "I accidentally deleted the SMS, can you resend the verification link?",
                "Which app store link should I use to download the support software?",
                "Is this the same link they use for KYC updates?",
                "Can you text me the link to the payment gateway?",
                "I’m at the login page, but it looks different—can you send me the direct link?",
                "Where do I find the OTP? Is it in my email or my messages?",
                "I clicked 'Verify' but nothing happened, should I try clicking it again?",
                "My phone is asking for a 'Passcode'—is that my ATM PIN or something else?",
                "The battery is at 2%, let me find my charger before the phone dies!",
                "I think I put the wrong number in, let me start the whole process over.",
                "Wait, my screen just went black! Give me a minute to restart it.",
                "Can you explain what a 'UPI' is again? I've never used this before.",
                "Is there a way to do this tomorrow morning? I'm very tired and confused.",
                "My neighbor just walked in, I have to hide the phone, stay on the line!",
                "I typed the code but it says 'Expired,' can you send me a new one?"
            ]))
        
        if "Incentive & Job Traps" in tactics:
            return self.synthesizer.apply_typo(random.choice([
                "I really need the extra money. Is it really just liking YouTube videos for salary?",
                "I joined the Telegram group but I am not sure how to start the tasks. Can you show me?",
                "Will I get my bonus today? I am ready to work hard.",
                "Is there a registration fee? I can pay it right now if you give me the link.",
                "I saw your ad on Instagram. Is this a permanent work-from-home position?",
                "My friend told me they earned 5000 yesterday. Can I also start with the premium tasks?",
                "Do I need to download a specific app to track my daily earnings?",
                "I am logged into the portal, but it says my balance is zero. What should I do?",
                "Can you send me the official UPI ID for the security deposit?",
                "I want to be a VIP member. Does that mean I get paid every hour?",
                "Is there a WhatsApp group where you post the new tasks?",
                "I’m ready to start the trial. Should I send the screenshot of the liked video here?",
                "My bank rejected the first transfer. Do you have another account I can try?",
                "Is this part of the 'Viksit Bharat' digital employment scheme?",
                "I have my resume ready. Should I upload it to the link you sent?",
                "Can I earn more if I refer my family members to this job?",
                "The Telegram admin is asking for a code. Is that the one you sent me?",
                "I don't have a laptop, can I do all these tasks on my mobile phone?",
                "Which company is hiring? I want to tell my wife I got a good job.",
                "Do you pay through Google Pay or PhonePe? I have both ready.",
                "The website says 'KYC Pending.' Can you send me the link to fix that?",
                "I am very hardworking. Can I do 20 tasks today to get a double bonus?",
                "Wait, the merchant name on the UPI is different. Is that your company name?",
                "Is there a training video I should watch before I start the tasks?",
                "Can I talk to your manager? I want to ask about the monthly salary package.",
                "I just finished the first task. When will the 50 rupees show up in my wallet?",
                "The app is asking for 'Merchant Verification.' What does that mean?",
                "I am confused about the 'Task 3' payment. Do I have to pay first to get the reward?",
                "Can you give me your personal mobile number in case I get stuck on a task?",
                "I want to make sure this is real. Can you send a photo of your office ID?",
                "Is this a government-approved data entry job?",
                "I tried the link but it says 'Server Busy.' Do you have a mirror link?",
                "Do I get a certificate after I finish the 10-day training?",
                "My bank says this UPI ID is a 'High Risk' account. Is that a mistake?",
                "I have 2000 rupees ready for the 'Prepaid Task.' Where should I send it?",
                "If I finish the work early, can I get my payment by this evening?",
                "The portal is asking for a 'Withdrawal Password.' How do I set that up?",
                "Can you show me a screenshot of someone else who got paid today?",
                "I'm using a shared phone. Is it okay if I log in from a different device?",
                "Is there a limit to how many YouTube videos I can like per day?",
                "The Telegram channel is muted. How do I message the receptionist?",
                "I am very excited to work with you. This will help my family a lot.",
                "Can I pay the deposit using a credit card or only UPI?",
                "Does the job involve any calling, or is it just clicking links?",
                "I’m at the 'Recharge' screen. Which plan should I pick for the best bonus?",
                "Can you send me the QR code for the task activation?",
                "I tried to join the group but it says 'Invite Expired.' Can I have a new link?",
                "Is there any age limit? My 18-year-old son also wants to join.",
                "I missed the morning task. Can I make it up by doing double tonight?",
                "I just sent the 1000 rupees. Please check and activate my VIP account!"
            ]))
            
        if "Authority Impersonation" in tactics:
            return self.synthesizer.apply_typo(random.choice([
                "I didn't know the head office would call me personally! Thank you for helping an old man.",
                "Yes sir, I see you are from the bank. I was just about to go to the branch.",
                "Is this the verification department? I have my Aadhaar card ready.",
                "Please don't freeze my account! I need that money for my daughter's wedding.",
                "The local police station is very far. Can we settle this online right now?",
                "Is there a case number I should give to my lawyer?",
                "My bank manager never mentioned this. Are you from the Mumbai main office?",
                "I am looking at my messages, but there are so many. Is it a 6-digit one?",
                "Wait, my phone says 'Do not share'. Is it safe to give you this code?",
                "The screen just refreshed and the code disappeared. Can you send it one more time?",
                "Is this about that legal notice? I am very worried about my bank account being frozen.",
                "I promise I didn't do anything wrong! What do I need to do to stop the police from coming?",
                "Oh no, I don't want to go to jail! Please help me, I have a family.",
                "Can you send me a photo of your police ID card so I can show my wife?",
                "Wait, why is the CBI calling me? I’m just a normal person!",
                "Is there a fine I can pay to close this file immediately?",
                "I have the OTP now. Should I read it out or type it into the link?",
                "The app is asking for my ATM PIN to 'Reset.' Is that part of the process?",
                "Can you give me your direct department extension in case the call drops?",
                "I'm at the ATM now. Which button should I press to 'Cancel the Block'?",
                "The message says 'Account Debited.' Why is my money being moved?",
                "Is there a PDF file of the warrant you can send me on WhatsApp?",
                "My phone says 'Suspected Spam,' but I know you are the real officer.",
                "Can I speak to your senior? I want to explain that it wasn't me!",
                "Which branch are you calling from? I will come there tomorrow morning.",
                "I'm typing the UPI PIN now. Will this confirm my identity to the RBI?",
                "The caller ID says 'Delhi Police,' but your accent sounds different. Is this a special task force?",
                "I'm trying to open the link you sent, but it says 'Malicious Site.' Is your server down?",
                "Do you need my Pan Card number as well to verify the bank details?",
                "I am very confused. Why does the 'Refund' require me to send money first?",
                "The message says 'Unauthorized Access detected.' Is that why you called?",
                "I will do whatever you say, just please don't let them arrest me!",
                "Can you send the 'NOC' letter to my email address once this is finished?",
                "Is this related to the electricity bill I paid last month?",
                "I'm on the 'AnyDesk' app now. What is the 9-digit code you need?",
                "Wait, my screen is moving on its own! Is that you helping me?",
                "If I pay the 'Security Fee,' will my account be unblocked in 5 minutes?",
                "The bank says my KYC is expired. Can you update it from your computer?",
                "Is there a toll-free number for the Cyber Cell I can verify this with?",
                "Why do you need my wife's account details too? Is her account also at risk?",
                "I have 50,000 in that account. Please tell me it’s still safe!",
                "I am writing down your name and designation. Can you repeat them slowly?",
                "The OTP just came. It says 'Transaction of 10,000.' Is that a test amount?",
                "Is there a way to do a video call so I can see the police station?",
                "I don't have a smartphone. Can I give you the code over this normal call?",
                "My son is a lawyer. He is asking for the Section number of this crime.",
                "Is this the CBI headquarters in Delhi? My brother works near there.",
                "I'm at the 'Add Beneficiary' page. What name should I put for the account?",
                "The app says 'Daily Limit Reached.' Do you have another UPI ID I can use?",
                "Please hurry, I don't want my neighbors to see the police car at my house!"
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
