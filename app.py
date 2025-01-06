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

# Приветственное сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Привет! 👋\n\n"
        "Я навигационный бот. 🌍 Напиши мне адрес, название места или любой запрос, и я помогу найти его на Google Maps! 🗺️\n\n"
        "Пример запросов:\n"
        "📍 Адрес: 1600 Amphitheatre Parkway\n"
        "🏙️ Место: Эйфелева башня\n"
        "🚇 Станция метро: Diagonal\n"
        "Попробуй! 😉"
    )
    await update.message.reply_text(welcome_message)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    print(f"Получен запрос: {query}")  # Для отладки

    try:
        # Кодируем запрос для корректного формирования URL
        encoded_query = quote(query)

        # Логика формирования URL
        is_address = any(char.isdigit() for char in query)
        is_street = any(word in query.lower() for word in ["street", "avenue", "road", "boulevard", "drive", "lane", "carrer", "calle"])
        is_metro = any(word in query.lower() for word in ["station", "metro", "underground", "subway", "diagonal", "sagrera", "verdaguer"])
        is_place = any(word in query.lower() for word in ["plaza", "square", "park", "area"])

        if is_address or is_metro:
            google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={encoded_query}"
            response = f"📍 Адрес/метро найдено!\n🌍 Карты: {google_maps_url}"
        elif is_street or is_place:
            google_maps_url = f"https://www.google.com/maps/search/{encoded_query}"
            response = f"🏙️ Улица/место найдено!\n🌍 Карты: {google_maps_url}"
        else:
            google_maps_url = f"https://www.google.com/maps/search/{encoded_query}+near+me"
            response = f"🔍 Поиск ближайшего места по запросу: {query}\n🌍 Карты: {google_maps_url}"

        await update.message.reply_text(response)

    except Exception as e:
        error_message = f"⚠️ Произошла ошибка при обработке вашего запроса: {e}"
        await update.message.reply_text(error_message)

# Функция запуска Telegram-бота
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
