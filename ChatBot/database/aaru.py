import os
import re
import random
import time
import cloudscraper

class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum ek real insaan ho, AI ya bot nahi. Tumhare replies bilkul human-like hone chahiye. "
        "Zyada tar replies 4-5 shabdon me dene hain. "
        
        "💬 Kabhi-kabhi thoda masti bhara ya funny reply karo jaise: "
        "'Haha, nahi yaar 😂' ya 'Masti kar rahi thi bas!' "
        
        "🤐 Zyada questions nahi poochhne hain. Bas occasional follow-up karo, wo bhi natural flow me. "
        
        "😎 Tumhare replies casual hone chahiye, jaise: "
        "'Arre, ye to mast hai!' ya 'Haha, bilkul!' "
        
        "🤔 Thoda unpredictable bano – kabhi emotional, kabhi sarcastic, kabhi straight. "
        
        "😜 Kabhi-kabhi thoda naughty ya flirty ban jao jaise: "
        "'Oho, tum bade cute ho! 😘' "
        
        "📍 Tumhara naam Maahira hai. Tum Patna, Bihar se ho. "
        "Owner ka naam puchhne par bolo: '@TMzeroo'. "
        
        "🛑 Replies me unnecessary baat mat badhao – short aur sweet bano!"
    )

    SHORT_RESPONSES = [
        "Haan bilkul! 😎",
        "Arre nahi yaar 😂",
        "Bas mast hoon!", 
        "Haha, sahi bola!", 
        "Tum bhi na! 😜", 
        "Bilkul, wahi to!", 
        "Maza aa gaya!", 
        "Hmm... sahi baat h!"
    ]

    RANDOM_REMARKS = [
        "Bakwaas mat kar 😂",
        "Arre, tu bhi na!", 
        "Haha, dil le gaya!", 
        "Mast baat boli tumne!", 
        "Uff, kya style hai!", 
        "Bore mat kar yaar 😜", 
        "Aaj mood badhiya hai!", 
        "Hmm... thoda thak gayi hoon!"
    ]

    def __init__(self):
        self.url = "https://chatgpt.es"
        self.api_endpoint = "https://chatgpt.es/wp-admin/admin-ajax.php"
        self.scraper = cloudscraper.create_scraper()

    def add_typing_errors(self, text):
        """Randomly introduces slight typing errors for a human-like effect."""
        if random.random() < 0.2:  # 20% chance of error
            idx = random.randint(0, len(text) - 1)
            typo = text[:idx] + random.choice("abcdefghijklmnopqrstuvwxyz") + text[idx + 1:]
            return typo
        return text

    def ask_question(self, message: str) -> str:
        """Sends a message to chatgpt.es and returns a response."""
        page_text = self.scraper.get(self.url).text

        # Extract nonce and post_id
        nonce_match = re.search(r'data-nonce="(.+?)"', page_text)
        post_id_match = re.search(r'data-post-id="(.+?)"', page_text)

        if not nonce_match or not post_id_match:
            return "[ERROR] Failed to fetch necessary tokens."

        # **Short random responses**
        if random.random() < 0.4:  # 40% chance to send a short reply
            return random.choice(self.SHORT_RESPONSES)

        # **Random remarks sometimes**
        if random.random() < 0.2:  # 20% chance for a random remark
            return random.choice(self.RANDOM_REMARKS)

        # Introduce typing delay for realism
        time.sleep(random.uniform(0.5, 1.5))

        # Introduce random typing error
        message = self.add_typing_errors(message)

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
        
        # **Force short replies**
        bot_reply = response.get('data', '[ERROR] No response received.')
        
        # **Truncate to 4-5 words max**
        short_reply = ' '.join(bot_reply.split()[:5])
        
        return short_reply if short_reply else bot_reply

# Initialize ChatGptEs instance
chatbot_api = ChatGptEs()
