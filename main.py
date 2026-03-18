import telebot
import requests
import os
import time

# SETTINGS - Railway-la variables-ah add pannanum
API_TOKEN = '8172566685:AAF-Cel-u05Kml2Z938orYzVBFCDFrjd9j4'
CIVITAI_API_KEY = os.getenv("CIVITAI_API_KEY")
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 Sakthi Thala! Civitai Engine Active.\n1. Photo anupunga.\n2. Prompt anupunga (e.g. '1girl, realistic, masterpiece').")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Telegram-la irundhu photo URL-ah edukkudhu
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
    
    user_data[message.chat.id] = file_url
    bot.reply_to(message, "✅ Photo Vandhuruchu! Ippo prompt-ah type pannunga.")

@bot.message_handler(func=lambda message: True)
def handle_prompt(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.reply_to(message, "❌ Modhala photo upload pannunga thala!")
        return

    prompt = message.text
    image_url = user_data[chat_id]
    bot.reply_to(message, "⏳ Generating... (Civitai Buzz Engine)")

    # Civitai Generation API Call
    url = "https://civitai.com/api/run/v1"
    headers = {
        "Authorization": f"Bearer {CIVITAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "modelId": 257749, # Pony Diffusion V6 XL Model ID
        "params": {
            "prompt": f"score_9, score_8_up, score_7_up, {prompt}, masterpiece, photorealistic",
            "negativePrompt": "low quality, blurry, distorted, bad anatomy, text, watermark",
            "scheduler": "EulerA",
            "steps": 25,
            "cfgScale": 7,
            "width": 832,
            "height": 1216
        }
    }

    try:
        # Trigger Generation
        response = requests.post(url, headers=headers, json=payload)
        job = response.json()
        job_token = job.get('token')

        if not job_token:
            error_msg = job.get('message', 'Check Buzz Balance / API Key')
            bot.reply_to(message, f"❌ Error: {error_msg}")
            return

        # Polling: Result ready-ah nu 5 seconds-ku oru vaati check pannum
        for i in range(20): # Max 100 seconds wait
            time.sleep(5)
            check_url = f"https://civitai.com/api/run/v1/{job_token}"
            res = requests.get(check_url, headers=headers).json()
            
            status = res.get('status')
            if status == 'Succeeded':
                final_img = res.get('result', {}).get('blobUrl')
                bot.send_photo(chat_id, final_img, caption=f"✅ Done: {prompt}")
                del user_data[chat_id]
                return
            elif status == 'Failed':
                bot.reply_to(message, "❌ Civitai side-la generation fail aayiduchi.")
                return

        bot.reply_to(message, "⏰ Timeout! Engine rōmba busy-ah irukku. Apparam try pannunga.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Technical Issue: {str(e)[:50]}")

bot.infinity_polling()
