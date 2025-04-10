import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatAction, ChatMembersFilter  
from ChatBot import app
from ChatBot.database import is_chatbot_enabled, enable_chatbot, disable_chatbot, chatbot_api


# ✅ Text filter for chatbot
async def text_filter(_, __, m: Message):
    """Filters valid chatbot messages."""
    return (
        bool(m.text)
        and len(m.text) <= 69
        and not m.text.startswith(("!", "/"))
        and (not m.reply_to_message or m.reply_to_message.reply_to_message_id == m._client.me.id)
    )

chatbot_filter = filters.create(text_filter)


# ✅ Chatbot handler (DM me always + Group me toggle)
@app.on_message(
    ((filters.text & chatbot_filter) | filters.mentioned)  
    & ~filters.bot  
    & ~filters.sticker
)
async def chatbot(_, message: Message):
    """Replies in DM always and in groups based on toggle."""
    chat_id = message.chat.id

    if message.chat.type == "private" or await is_chatbot_enabled(chat_id) or message.mentioned:
        await app.send_chat_action(chat_id, ChatAction.TYPING)
        reply = chatbot_api.ask_question(
            message.text,
            reply_to=message.reply_to_message.from_user.first_name if message.reply_to_message else None
        )
        await message.reply_text(reply or "❖ ChatBot Error. Contact @NoxxNetwork.")


# ✅ Enable/Disable button (Group ke liye)
@app.on_message(filters.command(["chatbot"]) & filters.group & ~filters.bot)
async def chatbot_toggle(_, message: Message):
    """Shows chatbot enable/disable options in groups."""
    
    # ✅ Admin list fetch karo
    admins = []
    async for member in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):  
        admins.append(member.user.id)
    
    if message.from_user.id not in admins:
        await message.reply_text("❖ You are not an admin.")
        return

    # ✅ Button with toggle options
    is_enabled = await is_chatbot_enabled(message.chat.id)
    btn_text = "🚫 Disable" if is_enabled else "✅ Enable"
    btn_callback = f"rmchat_{message.chat.id}" if is_enabled else f"addchat_{message.chat.id}"

    await message.reply_text(
        f"❖ Chatbot is currently {'enabled' if is_enabled else 'disabled'}.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(btn_text, callback_data=btn_callback)]
        ]),
    )


# ✅ Callback handler with toggle system
@app.on_callback_query(filters.regex(r"^(addchat|rmchat)_"))
async def chatbot_callback(_, query: CallbackQuery):
    """Handles enabling/disabling chatbot in groups."""
    
    chat_id = int(query.data.split("_")[1])
    user_id = query.from_user.id

    try:
        # ✅ Admin check
        admins = []
        async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):  
            admins.append(member.user.id)

        if user_id not in admins:
            await query.answer("❖ You are not an admin.", show_alert=True)
            return

        # ✅ Toggle system with button intact
        if "addchat" in query.data:
            await enable_chatbot(chat_id)
            await query.message.edit_text(
                f"✅ Chatbot enabled by {query.from_user.mention}.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚫 Disable", callback_data=f"rmchat_{chat_id}")]
                ])
            )
        
        elif "rmchat" in query.data:
            await disable_chatbot(chat_id)
            await query.message.edit_text(
                f"🚫 Chatbot disabled by {query.from_user.mention}.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Enable", callback_data=f"addchat_{chat_id}")]
                ])
            )

        # ✅ Callback confirm karo
        await query.answer()

    except Exception as e:
        await query.answer(f"❖ Error: {str(e)}", show_alert=True)
