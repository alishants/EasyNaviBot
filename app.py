from flask import Flask, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading
import asyncio

# Flask-приложение для мини-приложения
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Убедитесь, что index.html находится в папке templates

# Telegram-бот
TOKEN = "8197947754:AAG0EtbpnqKGU3w0P7Sy_3AA4wko1Ps-ZL4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введите запрос, чтобы я нашёл это место на Google Maps.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    google_maps_url = f"https://www.google.com/maps/search/{query}"
    await update.message.reply_text(f"Вот ваша ссылка: {google_maps_url}")

def start_bot():
    # Запуск Telegram-бота
    asyncio.set_event_loop(asyncio.new_event_loop())  # Создаём новый цикл событий
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    # Запускаем Telegram-бота в отдельном потоке
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    # Запускаем Flask-приложение
    app.run(host="0.0.0.0", port=5000)
