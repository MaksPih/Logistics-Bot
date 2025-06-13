import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.config import BOT_TOKEN
from bot.handlers import info
from bot.handlers import contact
from bot.handlers import delivery
from bot.services.database import init_db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(info.router)
dp.include_router(contact.router)
dp.include_router(delivery.router)
    
# Головне меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Розрахувати вартість доставки")],
        [KeyboardButton(text="🚛 Відстежити замовлення")],
        [KeyboardButton(text="📋 Детальніше про TransLine Logistics"), KeyboardButton(text="☎️ Контакти та Зв’язок з менеджером")]
    ],
    resize_keyboard=True
)

@dp.message(lambda msg: msg.text == "/start")
async def start_handler(message: types.Message):
    if message.text == "/start":
        await message.answer(
            "Вас вітає компанія *TransLine Logistics*! 🚛\n"
            "Ми допоможемо вам швидко та безпечно перевезти вантажі будь-якої складності.\n"
            "Оберіть дію з меню нижче 👇",
            reply_markup=main_menu,
            parse_mode="Markdown"
        )

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    @dp.startup()
    async def on_startup(bot: Bot):
        print("✅ Бот успішно запущено.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())