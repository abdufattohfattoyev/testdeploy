from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n"
                         f"Valyuta botiga xush kelibsiz!")


@dp.message_handler(commands=['valyuta'])
async def valyuta(message: types.Message):
    url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
    response = requests.get(url).json()

    javob = ""
    for val in response:
        if val['Ccy'] in ['USD', 'EUR', 'RUB']:
            javob += f"{val['Ccy']}: {val['Rate']}\n"

    await message.reply(javob if javob else "Valyuta ma'lumotlari topilmadi.")