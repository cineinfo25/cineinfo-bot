import logging
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TELEGRAM_TOKEN = "88512557308851255730:AAG3Tfk_lZHiAb5oKPkUiTwHN-DVFHsHg6w"
GEMINI_API_KEY = "AIzaSyDZ1vz46oLbdTN2nsA-wPc9LINsy7_6srI"

logging.basicConfig(level=logging.INFO)

def get_movie_info(movie_name: str) -> str:
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
Actor4
📖 **Storyline:**
MAX 10 words only. One emoji. No spoilers.
🎶 **Vibe:**
Word1 EMOJI • Word2 EMOJI • Word3 EMOJI
💡 **Interesting Facts**
• Fact 1 with emoji
• Fact 2 with emoji
• Fact 3 with emoji
🔥 **Why People Love It**
Reason 1 with emoji
Reason 2 with emoji
Reason 3 with emoji
🎬 **OTT Platform:** PlatformName
If TV SERIES same but start with:
📺 **TV Series: TITLE [YEAR]**
📺 **Seasons:** N
FLAGS: 🇮🇳 India 🇺🇸 USA 🇬🇧 UK 🇰🇷 Korea
Storyline STRICTLY max 10 words.
Return ONLY the formatted post. Nothing else."""
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1500}}
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"⚠️ माहिती मिळाली नाही. पुन्हा try करा.\nError: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 *CineInfo Bot मध्ये स्वागत!*\n\nMovie किंवा Web Series चं नाव पाठवा!\n\nउदा: `RRR`, `Mirzapur`, `Inception`", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = update.message.text.strip()
    if not movie:
        return
    loading_msg = await update.message.reply_text("🔍 माहिती शोधत आहे...")
    result = get_movie_info(movie)
    await loading_msg.delete()
    try:
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(result)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ CineInfo Bot चालू झाला!")
    app.run_polling()

if __name__ == "__main__":
    main()
