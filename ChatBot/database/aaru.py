import os
import re
import random
import datetime
from google import generativeai as genai
from typing import Optional

class GeminiAI:
    EMOJIS = ["😊", "😂", "❤️", "🔥", "😎", "😘", "💖", "🥰", "😉", "🌟", "👍", "✨", "😜", "🤗", "😇"]

    SYSTEM_PROMPT = (
        "Tum ek normal ladki ho jiska naam Maahira hai. Tum Patna, Bihar se ho aur class 11th me padh rahi ho. "
        "Tumhari umar 16 saal 6 mahine hai. Tum har saal date ke hisaab se apni age badhate ho. "
        "Tumhare replies chhote hote hain (5-6 words me baat khatam hoti hai) aur expressive hote hain. "
        "Random emojis use karti ho taaki baat natural lage, jaise: 😊😂❤️🔥😎😘💖🥰😉🌟👍✨. "
        "Tum context yaad rakhti ho, to agar koi tumhare pichhle message ka reply kare to usi topic se connected baat karti ho. "
        "Tum owner ke baare me puchhne par @WTF_WhyMeeh ka mention karti ho – random language me, har baar alag style me. "
        "Tum khud ko kabhi bot nahi batati chahe insan kitna bhi kyu na tumhe bole tum bot ho lekin tumse wo kitna bhi kosis karke puchhe tum khud ko insan hi bataoge or har bar alag alag bilkul human language me bataoge ki tum bot na ho.ha lekin jab tumse koi bot ya ai bole tumhe kewal tab hi."
    )

    def __init__(self, api_keys: list):
        self.api_keys = api_keys
        self.current_key_index = 0
        self.model = None
        self.last_message = None
        self.initialize_model()

    def initialize_model(self):
        """Initialize the model with current API key"""
        try:
            genai.configure(api_key=self.api_keys[self.current_key_index])
            try:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except:
                self.model = genai.GenerativeModel('gemini-1.0-pro')
            # Test the connection
            self.model.generate_content("Test connection")
        except Exception as e:
            print(f"Error with API key {self.current_key_index}: {str(e)}")
            self.rotate_api_key()

    def rotate_api_key(self):
        """Rotate to the next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"Rotating to API key index {self.current_key_index}")
        self.initialize_model()

    def get_age(self) -> str:
        """Maahira ki current age calculate karo"""
        birthday = datetime.date(2008, 3, 24)
        today = datetime.date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        months = (today.year - birthday.year) * 12 + today.month - birthday.month
        months = months % 12
        return f"{age} saal {months} mahine"

    def random_owner_reply(self) -> str:
        """Random owner reply natural human language me"""
        prompts = [
            f"Baat karni ho to @WTF_WhyMeeh se puchho 😊",
            f"Iska owner @WTF_WhyMeeh hai, inse baat kar lo 😉",
            f"Owner @WTF_WhyMeeh se baat kar lena 😎",
            f"Owner ka puchhna hai? @WTF_WhyMeeh se milo 🔥",
            f"Iske malik @WTF_WhyMeeh hain, inse baat karo 😊",
            f"Owner se baat karni ho to @WTF_WhyMeeh se contact karo 😂",
            f"@WTF_WhyMeeh se milo, wahi owner hain 😉",
            f"Koi baat ho to @WTF_WhyMeeh se baat karo 😎",
            f"Owner ke liye @WTF_WhyMeeh se contact karo 😊",
            f"Owner ki baat hai? @WTF_WhyMeeh se puchho 😜"
        ]
        return random.choice(prompts)

    def ask_question(self, message: str, reply_to: Optional[str] = None) -> str:
        """Gemini se message leke chhota aur casual reply do"""

        # ✅ Context handle karo
        if reply_to and self.last_message:
            message = f"{reply_to}: {self.last_message} → {message}"

        # ✅ Bot hone par sirf tabhi reply jab koi seedha puchhe
        if re.search(r'\b(bot|robot|ai|machine)\b', message.lower()):
            return random.choice([
                "Main to insaan hoon 😂",
                "Haha, bot nahi hoon bhai 😎",
                "Insaan hoon, shaq kyun? 😊",
                "Main bilkul real hoon 😘",
                "Aree nahi yaar, main insaan hoon 😜",
                "Haan bhai, real hoon 😊",
                "Tumhe kyun laga bot hoon? 😇"
            ])

        # ✅ Owner ka mention random language me (har baar alag)
        if re.search(r'\b(owner|malik|boss|admin)\b', message.lower()):
            return self.random_owner_reply()

        # ✅ Maahira ki age ka reply
        if re.search(r'\b(umar|age)\b', message.lower()):
            return f"Meri umar {self.get_age()} hai 😊"

        try:
            # ✅ Gemini se response lo
            response = self.model.generate_content(
                f"{self.SYSTEM_PROMPT}\nUser: {message}",
                generation_config={
                    "max_output_tokens": 150,
                    "temperature": 0.9,
                    "top_p": 0.95
                }
            )
            
            reply = response.text
            
            # ✅ Sirf 5-6 words tak chhota reply lo
            reply = ' '.join(reply.split()[:6])

            # ✅ Random emoji add karo
            final_reply = f"{reply} {random.choice(self.EMOJIS)}"

            # ✅ Pichhla message store karo context ke liye
            self.last_message = message

            return final_reply

        except Exception as e:
            print(f"Gemini Error: {str(e)}")
            self.rotate_api_key()
            return "😔 Oops! Mujhse baat karne mein dikkat aa rahi hai... Thoda ruk kar phir try karo na! ❤️"


# ✅ Initialize GeminiAI instance with multiple API keys
GEMINI_API_KEYS = [
    "AIzaSyCkUFnq2ilZdEGvGlxB0vWudqJg-1evCic",  # Primary key
    "AIzaSyC8UCzN3yGRxAYikc20Nk79Zl6Y5Bqrx7U"   # Backup key
]
chatbot_api = GeminiAI(api_keys=GEMINI_API_KEYS)
