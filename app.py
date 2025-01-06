from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

app = Flask(__name__)

# Telegram Bot
TOKEN = "8197947754:AAG0EtbpnqKGU3w0P7Sy_3AA4wko1Ps-ZL4"
WEBHOOK_URL = "https://https://easynavibot.onrender.com/webhook"  # Замените your-render-url.com на ваш URL Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введите запрос, чтобы я нашёл это место на Google Maps.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    google_maps_url = f"https://www.google.com/maps/search/{query}"
    await update.message.reply_text(f"Вот ваша ссылка: {google_maps_url}")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot_app.bot)
    bot_app.process_update(update)
    return "OK", 200

@app.route("/")
def home():
    return render_template("index.html")  # Ваше мини-приложение

if __name__ == "__main__":
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Устанавливаем вебхук
    bot_app.bot.set_webhook(WEBHOOK_URL)
    app.run(host="0.0.0.0", port=5000)
