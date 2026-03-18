import telebot
import replicate
import os
import requests

# BOT TOKEN
API_TOKEN = '8172566685:AAF-Cel-u05Kml2Z938orYzVBFCDFrjd9j4'
bot = telebot.TeleBot(API_TOKEN)

# Replicate Token (Railway Variables-la irundhu edukkum)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 Sakthi Thala! AI Bot Active.\n1. Photo anupunga.\n2. Prompt anupunga (Edit panna).")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
    
    user_data[message.chat.id] = file_url
    bot.reply_to(message, "✅ Photo Vandhuruchu! Ippo prompt-ah type pannunga.")

@bot.message_handler(func=lambda message: True)
def handle_prompt(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.reply_to(message, "❌ Modhala photo upload pannunga!")
        return

    prompt = message.text
    image_url = user_data[chat_id]
    bot.reply_to(message, "⏳ AI Engine Processing... 20-30s aagum, wait pannunga!")

    try:
        # Replicate Client manual-ah setup panrom (401/422 errors avoid panna)
        client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        
        # Stable Version: lucataco/pony-diffusion-v6-xl
        output = client.run(
            "lucataco/pony-diffusion-v6-xl:8cdab211979535179a861f06f9c0922da0a63045610ecf1d0339d1000858d951",
            input={
                "prompt": f"score_9, score_8_up, score_7_up, {prompt}, masterpiece, realistic",
                "image": image_url,
                "negative_prompt": "score_4, score_5, score_6, low quality, bad anatomy, text, watermark",
                "strength": 0.7,
                "guidance_scale": 7.5
            }
        )

        if output and len(output) > 0:
            bot.send_photo(chat_id, output[0], caption=f"✅ Result: {prompt}")
            del user_data[chat_id]
        else:
            bot.reply_to(message, "❌ AI result tharala. Replicate credits/billing check pannunga.")

    except Exception as e:
        # Error message short-ah purira maadhiri varum
        bot.reply_to(message, f"⚠️ Engine Issue: {str(e)[:100]}")

bot.infinity_polling()
