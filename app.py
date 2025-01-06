from flask import Flask, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import multiprocessing
import asyncio
from urllib.parse import quote

# Flask-приложение для мини-приложения
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Путь к вашему мини-приложению в папке templates

# Telegram-бот
TOKEN = "8197947754:AAG0EtbpnqKGU3w0P7Sy_3AA4wko1Ps-ZL4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введите запрос, чтобы я нашёл это место на Google Maps.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    # Кодируем запрос для корректного формирования URL
    encoded_query = quote(query)

    # Логика формирования URL
    is_address = any(char.isdigit() for char in query)
    is_street = any(word in query.lower() for word in ["street", "avenue", "road", "boulevard", "drive", "lane", "carrer", "calle"])
    is_metro = any(word in query.lower() for word in ["station", "metro", "underground", "subway", "diagonal", "sagrera", "verdaguer"])
    is_place = any(word in query.lower() for word in ["plaza", "square", "park", "area"])

    if is_address or is_metro:
        google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={encoded_query}"
    elif is_street or is_place:
        google_maps_url = f"https://www.google.com/maps/search/{encoded_query}"
    else:
        google_maps_url = f"https://www.google.com/maps/search/{encoded_query}+near+me"

    await update.message.reply_text(f"Вот ваша ссылка: {google_maps_url}")

def start_bot():
    # Создаём новый цикл событий
    asyncio.set_event_loop(asyncio.new_event_loop())
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    # Создаем процесс для Telegram-бота
    bot_process = multiprocessing.Process(target=start_bot)
    bot_process.start()

    # Запуск Flask-приложения
    app.run(host="0.0.0.0", port=5000)

    # Ожидаем завершения процесса Telegram-бота
    bot_process.join()
