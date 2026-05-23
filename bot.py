import logging
import logging
import requests
import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

TELEGRAM_TOKEN = os.getenv("8851255730:AAG3Tfk_lZHiAb5oKPkUiTwHN-DVFHsHg6w")
GEMINI_API_KEY = os.getenv("AIzaSyD531RXj134QhsO8ceTiZh6YWrl74NQkIk")

logging.basicConfig(level=logging.INFO)

def get_movie_info(movie_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""You are a movie/TV series expert for a Telegram channel. Give info about: "{movie_name}"
Return ONLY this formatted text (use **text** for Telegram bold):
If MOVIE:
🎬 **Movie: TITLE [YEAR] | CERTIFICATE**
📅 **Release Date:** DD Month YYYY
⭐ **IMDb Rating: X.X/10** ⭐
👥 Based on around **XXK user ratings** on IMDb.
🎭 **Genre:** #Genre1 • #Genre2 • #Genre3
🌐 **Language:** #Language
FLAG **Country:** #CountryName
🎬 **Director:** Name
✍️ **Writer:** Name
⭐ **Main Cast:**
Actor1 as Character1
Actor2 as Character2
Actor3
📖 **Storyline:**
MAX 10 words only. One emoji. No spoilers.
🎶 **Vibe:**
Word1 EMOJI • Word2 EMOJI • Word3 EMOJI
💡 **Interesting Facts**
• Fact 1 with emoji
• Fact 2 with emoji
🔥 **Why People Love It**
Reason 1 with emoji
Reason 2 with emoji
🎬 **OTT Platform:** PlatformName
FLAGS: 🇮🇳 India 🇺🇸 USA 🇬🇧 UK 🇰🇷 Korea
Return ONLY the post. Nothing else."""
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1500}}
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def start(update, context):
    update.message.reply_text("🎬 CineInfo Bot मध्ये स्वागत!\n\nMovie चं नाव पाठवा!")

def handle_message(update, context):
    movie = update.message.text.strip()
    loading = update.message.reply_text("🔍 शोधत आहे...")
    result = get_movie_info(movie)
    loading.delete()
    update.message.reply_text(result, parse_mode="Markdown")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    print("✅ Bot चालू झाला!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
