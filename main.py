import telebot
import replicate
import os
import requests

# BOT TOKEN
API_TOKEN = '8172566685:AAF-Cel-u05Kml2Z938orYzVBFCDFrjd9j4'
bot = telebot.TeleBot(API_TOKEN)

# Replicate Token (Railway Variables-la irundhu edukkum)
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 Sakthi Thala! Replicate Engine Active. \n1. Photo anupunga.\n2. Prompt anupunga (No Filters!).")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
    
    user_data[message.chat.id] = file_url
    bot.reply_to(message, "✅ Photo Uploaded! Ippo unga prompt-ah type pannunga. (E.g. 'Turn this person into a naked model' or 'Add a girl next to me').")

@bot.message_handler(func=lambda message: True)
def handle_prompt(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.reply_to(message, "❌ Photo innum varala thala!")
        return

    prompt = message.text
    image_url = user_data[chat_id]
    bot.reply_to(message, "⏳ Replicate Engine Running... High-quality result loading! (15-20s)")

    try:
        # Calling Pony Diffusion V6 XL via Replicate
        output = replicate.run(
            "lucataco/pony-diffusion-v6-xl:8cdab211979535179a861f06f9c0922da0a63045610ecf1d0339d1000858d951",
            input={
                "prompt": f"score_9, score_8_up, score_7_up, {prompt}, masterpiece, realistic",
                "image": image_url,
                "negative_prompt": "score_4, score_5, score_6, low quality, distorted face",
                "strength": 0.7, # Edits evalo deep-ah irukkanum nu idhu decide pannum
                "guidance_scale": 7.5
            }
        )

        if output:
            bot.send_photo(chat_id, output[0], caption=f"✅ Result for: {prompt}")
            del user_data[chat_id]
        else:
            bot.reply_to(message, "❌ AI Engine didn't return output. Check Replicate credits!")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

bot.infinity_polling()
