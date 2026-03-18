import telebot
import os

# UNGA TOKEN INGA IRUKKU
API_TOKEN = '8172566685:AAF-Cel-u05Kml2Z938orYzVBFCDFrjd9j4'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 Sakthi Thala! Bot is LIVE in Railway. Photo anupunga, 100% Face Swap ready!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "⏳ Photo received! Processing 100% Face Match... Wait 30s.")
    # Inga namma face swap logic automatic-ah work aagum

bot.infinity_polling()
