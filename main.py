from pyrogram.types.messages_and_media import message
import requests
from pyrogram import Client , filters
import os
from PIL import Image
from requests.api import patch

bot = Client(
    "telegraph",
    api_hash=os.environ.get("api_hash"),
    api_id=os.environ.get("api_id"),
    bot_token=os.environ.get("token")
)

'''
/tm - reply to a image or sticker

'''


@bot.on_message(filters.command("start"))
def start():
    message.reply_text("Hello")


@bot.on_message(filters.command("tm"))
def upload_media(_,message):
    if message.reply_to_message.media:
        path = message.reply_to_message.download()
        file = {
            ("media", open(path, 'rb'))
        }

        res = requests.post("https://telegra.ph/upload" , files=file)

        for x in res.json():
            if not "webp" in path:
                link = x['src']
                bot.send_message(message.chat.id , f"https://telegra.ph{link})")
                os.remove(path)
            else:
                sticker = Image.open(path).convert("RGB")
                sticker.save(f"{path}.jpg" , "jpeg")
                file = {
                    ("media", open(f"{path}.jpg" , 'rb'))
                }
                res = requests.post("https://telegra.ph/upload" , files=file)
                print(res.text)
                for x in res.json():
                    link = x['src']
                    bot.send_message(message.chat.id , f"https://telegra.ph{link}")
                    os.remove(f"{path}.jpg")
                    





bot.run()
