from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.contact_states import ContactForm

router = Router()

# Інлайн-кнопка для запуску FSM
contact_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Залишити заявку менеджеру", callback_data="contact_request")]
    ]
)

@router.message(lambda msg: msg.text == "☎️ Контакти та Зв’язок з менеджером")
async def contact_info(message: Message):
    text = (
        "📞 *Контактна інформація:*\n\n"
        "📍 Юридична адреса: м. Львів, вул. Промислова, 50/52\n"
        "📱 Центр підтримки 24/7: +38 (098) 465-84-97\n"
        "✉️ Email: info@transline-logistics.com\n\n"
        "🕘 *Графік роботи:*\n"
        "Пн–Пт: 08:00–18:00\n"
        "Сб: 09:00–15:00\n"
        "Нд: вихідний\n\n"
        "🔽 Залиште заявку, і наш менеджер зв'яжеться з вами:"
    )
    await message.answer(text, reply_markup=contact_inline_kb, parse_mode="Markdown")

# Натиснута інлайн-кнопка — початок FSM
@router.callback_query(F.data == "contact_request")
async def start_contact_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("👤 Вкажіть ваше ім’я:")
    await state.set_state(ContactForm.waiting_for_name)
    await callback.answer()

# Ім’я
@router.message(ContactForm.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Вкажіть номер телефону:")
    await state.set_state(ContactForm.waiting_for_phone)

# Телефон
@router.message(ContactForm.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("✉️ Напишіть короткий коментар або питання:")
    await state.set_state(ContactForm.waiting_for_comment)

# Коментар
@router.message(ContactForm.waiting_for_comment)
async def get_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    await message.answer(
        f"✅ Заявку надіслано!\n\n"
        f"👤 Ім’я: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"✉️ Коментар: {data['comment']}\n\n"
        f"Найближчим часом з вами зв’яжеться менеджер."
    )
    await state.clear()