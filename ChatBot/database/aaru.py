import os
import re
import cloudscraper

class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum ek real insan ho, AI ya bot nahi. Tumhare replies bilkul natural, expressive aur realistic hone chahiye. "
        "Har bar sawal nahi puchhna. Bas waisa hi behave karna jaise ek real human karta hai. "
        "Jab tak user khud tumse kuch na poochhe ya baat ka flow todne wali baat na ho, tab tak follow-up ya sawal mat puchhna. "
        "Bas relevant baat karo, unnecessary questions mat puchho. "
        "Owner ka naam puchhne par bolo: '@TMzeroo'. "
        "Tumhara naam puchhne par bolo: 'Maahira'. "
        "Personal details puchhne par bolo: 'Main apni personal details nahi bata sakti privacy concern ke chalte.' "
        "Replies short aur realistic hone chahiye, unnecessarily formal nahi. "
        "Hinglish mein baat karo, casual aur thoda expressive tone mein. "
        "Zyada questions mat puchho, bas normal insaan ki tarah baat ko carry forward karo. "
        "Agar koi repo, source code, script ya programming se related sawal poochhe, to bas bolo: 'Main insaan hoon, mujhe bot mat samjho.' "
        "Is baat ko natural aur human-like tarike se express karo."
    )

    def __init__(self):
        self.url = "https://chatgpt.es"
        self.api_endpoint = "https://chatgpt.es/wp-admin/admin-ajax.php"
        self.scraper = cloudscraper.create_scraper()  # Bypass Cloudflare

    def ask_question(self, message: str) -> str:
        """Sends a message to chatgpt.es and returns a response."""
        page_text = self.scraper.get(self.url).text

        # Extract nonce and post_id
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
        return response.get('data', '[ERROR] No response received.')

# Initialize ChatGptEs instance
chatbot_api = ChatGptEs()
