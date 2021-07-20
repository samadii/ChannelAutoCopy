import os

from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")
string = os.environ.get('SESSION')

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    Bot = TelegramClient(StringSession(string), APP_ID, API_HASH)
    Bot.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

@Bot.on(events.NewMessage(incoming=True, chats=FROM))
async def send(event):
    for i in TO:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await Bot.send_file(i, photo, caption = event.text, link_preview = False)
            elif event.media:
                try:
                    if event.media.webpage:
                        await Bot.send_message(i, event.text, link_preview = False)
                        return
                except:
                    media = event.media.document
                    await Bot.send_file(i, media, caption = event.text, link_preview = False)
                    return
            else:
                await Bot.send_message(i, event.text, link_preview = False)

        except Exception as e:
            print(e)

print("Bot has started.")
Bot.run_until_disconnected()
