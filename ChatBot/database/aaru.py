import os
import re
import random
import datetime
import cloudscraper


class ChatGptEs:
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

    def __init__(self):
        self.url = "https://chatgpt.es"
        self.api_endpoint = "https://chatgpt.es/wp-admin/admin-ajax.php"
        self.scraper = cloudscraper.create_scraper()
        self.last_message = None  # Pichhle message ka context store karne ke liye

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

    def ask_question(self, message: str, reply_to: str = None) -> str:
        """ChatGPT se message leke chhota aur casual reply do"""

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

        # ✅ Normal chatting ke liye
        page_text = self.scraper.get(self.url).text

        # ✅ Tokens fetch karo
        nonce_match = re.search(r'data-nonce="(.+?)"', page_text)
        post_id_match = re.search(r'data-post-id="(.+?)"', page_text)

        if not nonce_match or not post_id_match:
            return "[ERROR] Failed to fetch necessary tokens."

        payload = {
            'check_51710191': '1',
            '_wpnonce': nonce_match.group(1),
            'post_id': post_id_match.group(1),
            'url': self.url,
            'action': 'wpaicg_chat_shortcode_message',
            'message': f"{self.SYSTEM_PROMPT}\nUser: {message}",
            'bot_id': '0',
            'chatbot_identity': 'shortcode',
            'wpaicg_chat_client_id': os.urandom(5).hex(),
            'wpaicg_chat_history': None
        }

        response = self.scraper.post(self.api_endpoint, data=payload).json()
        reply = response.get('data', '[ERROR] No response received.')

        # ✅ Sirf 5-6 words tak chhota reply lo
        reply = ' '.join(reply.split()[:6])

        # ✅ Random emoji add karo
        final_reply = f"{reply} {random.choice(self.EMOJIS)}"

        # ✅ Pichhla message store karo context ke liye
        self.last_message = message

        return final_reply


# ✅ Initialize ChatGptEs instance
chatbot_api = ChatGptEs()
