import os
import random
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Poll
from motor.motor_asyncio import AsyncIOMotorClient
import google.generativeai as genai

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are Nova, an intelligent, friendly, and engaging AI assistant on Telegram. "
        "Your responses are natural, witty, clear, and helpful. Keep answers concise like a tech-savvy friend. "
        "When reading news or channel updates, provide insightful or cheerful commentary."
    )
)

# Connect to MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["nova_ai_db"]
users_col = db["users"]
chats_col = db["chat_history"]

# Initialize Bot & Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Helper: Save & Fetch Chat History
async def get_history(chat_id: int):
    doc = await chats_col.find_one({"chat_id": chat_id})
    return doc.get("history", []) if doc else []

async def save_history(chat_id: int, history: list):
    trimmed = history[-10:]
    await chats_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"history": trimmed}},
        upsert=True
    )

# Command: /start
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    await users_col.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id, "username": message.from_user.username}},
        upsert=True
    )
    
    welcome_text = (
        f"👋 **Hey {message.from_user.first_name}! I'm Nova.**\n\n"
        "I'm your AI companion for group chats and private DMs. Here is what I can do:\n\n"
        "💬 **AI Chat:** Talk freely in DMs or mention me in groups.\n"
        "📰 **Channel Auto-Reply:** I automatically comment on new linked channel posts!\n"
        "🎮 **Games & Fun:** Type `/game` to play trivia or word puzzles.\n"
        "📊 **Poll Creator:** Type `/poll` to quickly generate group polls."
    )
    
    bot_info = await bot.get_me()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Add to Group", url=f"https://t.me/{bot_info.username}?startgroup=true"),
            InlineKeyboardButton(text="🐙 GitHub Repo", url="https://github.com/MrBoss002/Nova")
        ],
        [
            InlineKeyboardButton(text="📢 Updates", url="https://t.me/ZeroTwoKerala"),
            InlineKeyboardButton(text="💬 Support", url="https://t.me/MrBoss002")
        ]
    ])
    
    await message.reply(welcome_text, parse_mode="Markdown", reply_markup=kb)

# Command: /game (Mini Games)
@dp.message(Command("game"))
async def game_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧠 AI Trivia Quiz", callback_data="game_trivia"),
            InlineKeyboardButton(text="🔤 Word Scramble", callback_data="game_scramble")
        ],
        [InlineKeyboardButton(text="🔒 Close", callback_data="close_game")]
    ])
    await message.reply("🎮 **Nova Game Hub**\nSelect a mini-game to play:", parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(F.data == "game_trivia")
async def start_trivia(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_poll(
        chat_id=callback.message.chat.id,
        question="🧠 Quick Trivia: Which framework allows async Telegram bots in Python?",
        options=["aiogram", "Django", "Flask", "Pandas"],
        type=Poll.QUIZ,
        correct_option_id=0,
        explanation="aiogram is the leading asynchronous framework for Telegram bot creation in Python!"
    )

@dp.callback_query(F.data == "game_scramble")
async def start_scramble(callback: types.CallbackQuery):
    await callback.answer()
    words = [("TELEGRAM", "E L E T G R M A"), ("PYTHON", "H T O Y P N"), ("DATABASE", "S A B A D A T E")]
    original, scrambled = random.choice(words)
    await callback.message.reply(
        f"🔤 **Word Scramble!**\n\nUnscramble this word: `{scrambled}`\n\n*(Type your answer in the chat!)*",
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "close_game")
async def close_game(callback: types.CallbackQuery):
    await callback.message.delete()

# Command: /poll
@dp.message(Command("poll"))
async def create_poll(message: types.Message):
    await bot.send_poll(
        chat_id=message.chat.id,
        question="🔥 How do you rate Nova AI?",
        options=["⚡ Super Fast & Smart", "👍 Pretty Good", "🤔 Needs More Features"],
        is_anonymous=False
    )

# Command: /clear
@dp.message(Command("clear"))
async def clear_memory(message: types.Message):
    await chats_col.delete_one({"chat_id": message.chat.id})
    await message.reply("🧹 My context memory for this chat has been reset!")

# Command: /stats (Admin Only)
@dp.message(Command("stats"))
async def stats_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    total_users = await users_col.count_documents({})
    await message.reply(f"📊 **Nova Bot Statistics**\n\n👥 **Total Registered Users:** {total_users}", parse_mode="Markdown")

# Admin Reply-To Broadcast
@dp.message(Command("broadcast"))
async def broadcast_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    reply_to = message.reply_to_message
    if not reply_to:
        await message.reply("⚠️ Please reply to the message or media you want to broadcast using `/broadcast`.")
        return

    users = await users_col.find({}).to_list(length=None)
    success, failed = 0, 0
    status_msg = await message.reply(f"📢 *Starting broadcast to {len(users)} users...*", parse_mode="Markdown")

    for user in users:
        try:
            await bot.copy_message(chat_id=user["user_id"], from_chat_id=message.chat.id, message_id=reply_to.message_id)
            success += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"📌 **Broadcast Completed**\n\n✅ **Success:** {success}\n❌ **Failed:** {failed}\n👥 **Total:** {len(users)}",
        parse_mode="Markdown"
    )

# Feature: Automatic Reply to Linked Channel Posts in Group
@dp.message(F.is_automatic_forward)
async def handle_channel_post(message: types.Message):
    post_text = message.text or message.caption
    if not post_text:
        return

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    prompt = f"A new channel post was published:\n\n'{post_text}'\n\nGive a short, friendly, and engaging comment about this update for the discussion group."

    try:
        response = await asyncio.to_thread(ai_model.generate_content, prompt)
        await message.reply(f"💡 {response.text}")
    except Exception as e:
        logging.error(f"Channel Auto-Reply Error: {e}")

# Main AI Chat Handler
@dp.message(F.text)
async def ai_chat_handler(message: types.Message):
    if message.text.startswith("/"):
        return

    bot_info = await bot.get_me()
    is_private = message.chat.type == "private"
    is_mentioned = bot_info.username in (message.text or "")
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id

    if is_private or is_mentioned or is_reply_to_bot:
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        clean_text = message.text.replace(f"@{bot_info.username}", "").strip()
        history = await get_history(message.chat.id)
        history.append({"role": "user", "parts": [clean_text]})

        try:
            chat_session = ai_model.start_chat(history=history[:-1])
            response = await asyncio.to_thread(chat_session.send_message, clean_text)
            reply_text = response.text

            history.append({"role": "model", "parts": [reply_text]})
            await save_history(message.chat.id, history)

            await message.reply(reply_text)
        except Exception as e:
            logging.error(f"AI Generation Error: {e}")
            await message.reply("Oops, my brain froze for a second! Try asking me again. 😊")

async def main():
    print("🚀 Nova AI Bot is online and listening...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
