import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Головне меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("📦 Розрахувати вартість доставки"),
    KeyboardButton("🚛 Відстежити замовлення")
)
main_menu.add(
    KeyboardButton("📋 Довідкова інформація"),
    KeyboardButton("☎️ Зв’язок з менеджером")
)

@dp.message()
async def start_handler(message: types.Message):
    if message.text == "/start":
        await message.answer(
            "Вас вітає логістична компанія!\n"
            "Оберіть дію з меню нижче 👇",
            reply_markup=main_menu
        )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(lambda _: print("Бот запущено"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())