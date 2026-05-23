import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("8851255730:AAG3Tfk_lZHiAb5oKPkUiTwHN-DVFHsHg6w")
GEMINI_API_KEY = os.getenv("AIzaSyD531RXj134QhsO8ceTiZh6YWrl74NQkIk")

logging.basicConfig(level=logging.INFO)

def get_movie_info(movie_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
You are a movie expert.
Give short movie info for: {movie_name}

Format:
🎬 Movie Name
⭐ IMDb Rating
📅 Release Year
🎭 Genre
🌐 Language
📖 Short Storyline
🔥 Why popular
📺 OTT Platform (if known)
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 CineInfo Bot मध्ये स्वागत! Movie नाव पाठवा.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = update.message.text.strip()
    await update.message.reply_text("🔍 शोधत आहे...")

    result = get_movie_info(movie)
    await update.message.reply_text(result)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ CineInfo Bot चालू झाला")
    app.run_polling()

if __name__ == "__main__":
    main()
