from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Головна кнопка
@router.message(lambda msg: msg.text == "📋 Детальніше про TransLine Logistics")
async def info_menu(message: Message):
    text = (
        "🏢 *TransLine Logistics* — сучасна транспортно-логістична компанія, яка спеціалізується на перевезенні вантажів по всій Україні та за її межами.\n\n"
        "🔹 Ми поєднуємо власний автопарк, цифрові рішення та професійну команду, щоб забезпечити клієнтам високу якість обслуговування.\n\n"
        "✅ Ефективність, прозорість і турбота про кожного клієнта — наші основні принципи."
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=main_info_kb)

# Інлайн-кнопки
main_info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📦 Послуги", callback_data="info_services")],
        [InlineKeyboardButton(text="🔧 Сервіс та цінності", callback_data="info_about")],
        [InlineKeyboardButton(text="🚛 Наш автопарк", callback_data="info_trucks")],
    ]
)

back_to_info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="info_back_section")]
    ]
)

# Цінності та інфраструктура
@router.callback_query(F.data == "info_about")
async def about_company(callback: CallbackQuery):
    text = (
        "🔧 *Сервіс та цінності*\n\n"
        "TransLine Logistics має власну станцію технічного обслуговування, обладнану за європейськими стандартами. "
        "Наші фахівці виконують своєчасне обслуговування як власного транспорту, так і техніки клієнтів-партнерів.\n\n"
        "СТО включає 12 спеціалізованих майданчиків: діагностику, зварювальні та фарбувальні пости, рихтування, шиномонтаж і автоматичну мийку. "
        "Обладнання дозволяє виконувати гарантійний ремонт вантажівок провідних брендів.\n\n"
        "💼 *Наші корпоративні цінності:*\n"
        "• Повага\n"
        "• Командний дух та ініціативність\n"
        "• Швидкість\n"
        "• Фокус на клієнта\n"
        "• Доступність"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_to_info_kb)
    await callback.answer()

# Послуги
@router.callback_query(F.data == "info_services")
async def services_info(callback: CallbackQuery):
    text = (
        "📦 *Ми надаємо такі послуги:*\n\n"
        "• Вантажні перевезення по Україні\n"
        "• Перевезення температурних вантажів\n"
        "• Доставка сипучих і рідких вантажів\n"
        "• Перевезення контейнерів\n"
        "• Обслуговування логістичних ланцюгів B2B\n"
        "• Можливість розрахунку маршруту через бота"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_to_info_kb)
    await callback.answer()

# Автопарк
@router.callback_query(F.data == "info_trucks")
async def trucks_info(callback: CallbackQuery):
    text = (
        "🚛 *Наш автопарк включає:*\n\n"
        "• Тентовані вантажівки (5–24 т)\n"
        "• Рефрижератори для температурних вантажів\n"
        "• Зерновози-самоскиди\n"
        "• Контейнеровози\n"
        "• Автоцистерни\n"
        "• Трали для негабаритних вантажів\n\n"
        "Компанія активно інвестує в оновлення автопарку. За останні роки придбано 80 нових авто — "
        "більше 80% з яких відповідають стандартам EURO-5 та EURO-6. "
        "Увесь транспорт обладнано GPS-моніторингом."
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_to_info_kb)
    await callback.answer()

# Назад
@router.callback_query(F.data.in_({"info_back_section"}))
async def back_to_info(callback: CallbackQuery):
    await callback.message.edit_text("🏢 *TransLine Logistics* — сучасна транспортно-логістична компанія, яка спеціалізується на перевезенні вантажів по всій Україні та за її межами.\n\n"
        "🔹 Ми поєднуємо власний автопарк, цифрові рішення та професійну команду, щоб забезпечити клієнтам високу якість обслуговування.\n\n"
        "✅ Ефективність, прозорість і турбота про кожного клієнта — наші основні принципи.", reply_markup=main_info_kb, parse_mode="Markdown")
    await callback.answer()