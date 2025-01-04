import asyncio
import logging
import sys
import requests
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from config import BOT_TOKEN, LASTFM_API_KEY
from button import menu

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"


@dp.message(Command('start'))
async def command_start(message: Message):
    await message.answer(f"Assalomu Aleykum, {html.bold(message.from_user.full_name)}!", reply_markup=menu)


@dp.message(F.text == 'Aloqa')
async def aloqa_handler(message: Message):
    await message.answer(
        text='Biz bilan bog‘lanish uchun: [Telegram](https://t.me/shokh_devloper)',
        reply_markup=menu
    )


@dp.message(F.text.contains("Qidirish"))
async def song_search_handler(message: Message):
    await message.answer("Iltimos, qo'shiq yoki ijrochi nomini yuboring:")


@dp.message()
async def search_song(message: Message):
    query = message.text
    params = {
        "method": "track.search",
        "track": query,
        "api_key": LASTFM_API_KEY,
        "format": "json",
    }
    try:
        response = requests.get(LASTFM_API_URL, params=params)
        data = response.json()


        if "results" in data and "trackmatches" in data["results"]:
            tracks = data["results"]["trackmatches"]["track"]
            if tracks:
                track = tracks[0]
                name = track["name"]
                artist = track["artist"]
                url = track.get("url", "URL topilmadi")
                await message.answer(
                    f"Topildi! 🎶\n"
                    f"Qo'shiq: {html.bold(name)}\n"
                    f"Ijrochi: {html.bold(artist)}\n"
                    f"👉 {url}"
                )
            else:
                await message.answer("Afsus, hech narsa topilmadi.")
        else:
            await message.answer("Afsus, hech narsa topilmadi.")
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("Xatolik yuz berdi. Keyinroq urinib ko‘ring.")




async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(main())

