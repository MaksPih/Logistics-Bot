from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

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

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Вас вітає логістична компанія!\n"
        "Ми допоможемо вам з перевезенням вантажів.\n"
        "Оберіть потрібну дію з меню нижче 👇",
        reply_markup=main_menu
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)