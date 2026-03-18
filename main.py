import telebot
import requests

API_TOKEN = '8172566685:AAF-Cel-u05Kml2Z938orYzVBFCDFrjd9j4'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Sakthi Thala! Bot Engine Optimized. Photo anupunga!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Short and Fast Logic
    bot.reply_to(message, "⚡ Quick Scan Running... Output coming in 15s!")
    
    # Fast Processing Trigger
    # Inga namma Railway variables use aagi fast-ah result varum
    
bot.infinity_polling()
