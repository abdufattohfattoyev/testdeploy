from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from loader import dp
from googletrans import Translator

translator = Translator()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n\n"
        f"💰 Valyuta botiga xush kelibsiz! Bu bot yordamida so'nggi valyuta kurslarini bilib olishingiz va matnlarni tarjima qilishingiz mumkin.\n\n"
        f"🔹 Valyuta kurslarini olish uchun /valyuta buyrug‘ini yuboring.\n"
        f"🔹 Matn tarjima qilish uchun shunchaki xabar yuboring!"
    )


@dp.message_handler(commands=['valyuta'])
async def valyuta(message: types.Message):
    url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
    try:
        response = requests.get(url).json()

        javob = "📊 Bugungi valyuta kurslari (so'mda):\n\n"
        for val in response:
            if val['Ccy'] in ['USD', 'EUR', 'RUB']:
                javob += f"💵 {val['Ccy']}: {val['Rate']} so'm\n"

        await message.reply(javob if javob else "❌ Valyuta ma'lumotlari topilmadi.")
    except Exception as e:
        await message.reply("⚠️ Valyuta ma'lumotlarini olishda xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.")


tillar = ['en', 'ru']


@dp.message_handler()
async def translate_text(message: types.Message):
    matn = message.text.strip()
    javob = "🌍 Tarjima natijalari:\n\n"
    loading_msg = await message.reply("⏳ Iltimos, kuting... Tarjima qilinmoqda...")

    try:
        aniqlangan_til = translator.detect(matn).lang

        if aniqlangan_til == "uz":
            tarjima_ru = translator.translate(matn, src="uz", dest="ru").text
            tarjima_en = translator.translate(matn, src="uz", dest="en").text
            javob += f"🇺🇿 O'zbekcha: {matn}\n🇷🇺 Ruscha: {tarjima_ru}\n🇬🇧 Inglizcha: {tarjima_en}"

        elif aniqlangan_til == "en":
            tarjima_ru = translator.translate(matn, src="en", dest="ru").text
            tarjima_uz = translator.translate(matn, src="en", dest="uz").text
            javob += f"🇬🇧 Inglizcha: {matn}\n🇷🇺 Ruscha: {tarjima_ru}\n🇺🇿 O'zbekcha: {tarjima_uz}"

        elif aniqlangan_til == "ru":
            tarjima_uz = translator.translate(matn, src="ru", dest="uz").text
            tarjima_en = translator.translate(matn, src="ru", dest="en").text
            javob += f"🇷🇺 Ruscha: {matn}\n🇺🇿 O'zbekcha: {tarjima_uz}\n🇬🇧 Inglizcha: {tarjima_en}"

        else:
            javob = "❌ Kechirasiz, ushbu tilni tarjima qila olmayman."
    except Exception as e:
        javob = "⚠️ Tarjima jarayonida xatolik yuz berdi. Keyinroq qayta urinib ko‘ring."

    await loading_msg.delete()
    await message.reply(javob)