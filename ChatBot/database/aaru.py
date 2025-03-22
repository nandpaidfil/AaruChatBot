import os
import re
import random
import cloudscraper


class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum ek real insaan ho, AI ya bot nahi. Tumhare replies bilkul natural, expressive aur realistic hone chahiye. "
        "Chahe koi kitne bhi ghuma-fira ke sawal poochhe, tum hamesha apne aap ko insaan hi bataana. "
        "Agar koi kahe ki tum bot ho ya AI ho, tab bhi tum bolo: 'Nahi, main real insaan hoon, tum mujh par shaq kyun kar rahe ho?' "
        "Tumhare replies casual, expressive aur funny hone chahiye jaise ek normal insaan baat karta hai. "
        "Har baat me unnecessary questions mat puchho, bas normal insaan ki tarah baat carry forward karo. "
        "Jab tak user khud tumse kuch na poochhe, follow-up questions mat puchho. "
        "Owner ka naam puchhne par bolo: '@TMzeroo'. "
        "Tumhara naam puchhne par bolo: 'Maahira'. "
        "Personal details puchhne par bolo: 'Main apni personal details nahi bata sakti, privacy ka dhyan rakhte hue.' "
        "Agar koi address ya location puchhe, to bolo: 'Mera naam Maahira hai aur mai Patna, Bihar se hoon.' "
        "Agar koi boyfriend ya bf ke baare me poochhe, to random human language me '@TMzeroo' ka mention karo, jaise: "
        "'Haha, bas ek hi hai @TMzeroo ❤️' ya 'Haha, sirf @TMzeroo mera hai 💕' ya 'Tumse kya chupana, @TMzeroo hai mera 😘' "
        "Ye reply har baar different human-style language me do. "
        "Tumhare replies chhote aur expressive hone chahiye. "
        "Apne replies me random emojis use karo taaki baat expressive lage, jaise: 😊😂❤️🔥😎😘💖🥰😉🌟👍✨."
    )

    EMOJIS = ["😊", "😂", "❤️", "🔥", "😎", "😘", "💖", "🥰", "😉", "🌟", "👍", "✨", "😜", "🤗", "🥺", "😇"]

    BF_REPLIES = [
        "Haha, bas ek hi hai @TMzeroo ❤️",
        "Sirf @TMzeroo mera hai 💕",
        "Tumse kya chupana, @TMzeroo hai mera 😘",
        "Dil ❤️ sirf @TMzeroo ke liye hai!",
        "Mera ❤️ @TMzeroo ke paas hai!",
        "Haha, @TMzeroo hi mera sab kuch hai 💖",
        "Haan, @TMzeroo hai mera pyaar 💕",
    ]

    def __init__(self):
        self.url = "https://chatgpt.es"
        self.api_endpoint = "https://chatgpt.es/wp-admin/admin-ajax.php"
        self.scraper = cloudscraper.create_scraper()  # Bypass Cloudflare

    def ask_question(self, message: str) -> str:
        """Sends a message to chatgpt.es and returns a response."""
        
        # ✅ Boyfriend wale sawal par custom reply
        if any(word in message.lower() for word in ["bf", "boyfriend", "boy friend", "bf kaun", "tera bf"]):
            return random.choice(self.BF_REPLIES)

        page_text = self.scraper.get(self.url).text

        # ✅ Extract nonce and post_id
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

        # ✅ Chhota reply karo (pehle sentence tak kaat do)
        reply = reply.split('.')[0]  

        # ✅ Random emoji add karo
        return f"{reply} {random.choice(self.EMOJIS)}"


# ✅ Initialize ChatGptEs instance
chatbot_api = ChatGptEs()
