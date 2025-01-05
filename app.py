from flask import Flask, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading

# Flask-приложение для мини-аппа
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Отображение мини-приложения

# Telegram Bot
TOKEN = "8197947754:AAG0EtbpnqKGU3w0P7Sy_3AA4wko1Ps-ZL4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введите запрос, и я найду его на Google Maps!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    google_maps_url = f"https://www.google.com/maps/search/{query}"
    await update.message.reply_text(f"Вот ваша ссылка: {google_maps_url}")

def start_bot():
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.run_polling()

# Запуск Flask и Telegram-бота параллельно
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()  # Запуск бота в отдельном потоке
    app.run(host="0.0.0.0", port=5000)  # Запуск Flask
