from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from bot.states.delivery_states import DeliveryForm
from bot.services.maps import get_route_data, build_static_map, calculate_cost
from bot.services.fuel import get_current_fuel_price
from bot.services.database import save_order
from bot.services.database import get_orders_by_user


router = Router()

# Типи авто
vehicle_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Тент", callback_data="vehicle_тент")],
        [InlineKeyboardButton(text="Рефрижератор", callback_data="vehicle_рефрижератор")],
        [InlineKeyboardButton(text="Зерновоз/самоскид", callback_data="vehicle_зерновоз/самоскид")],
        [InlineKeyboardButton(text="Трал/Негабарит", callback_data="vehicle_трал/негабарит")],
        [InlineKeyboardButton(text="Контейнеровоз", callback_data="vehicle_контейнеровоз")],
        [InlineKeyboardButton(text="Автоцистерна", callback_data="vehicle_автоцистерна")],
    ]
)

# Тоннаж
tonnage_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="5 т", callback_data="tonnage_5")],
        [InlineKeyboardButton(text="10 т", callback_data="tonnage_10")],
        [InlineKeyboardButton(text="15 т", callback_data="tonnage_15")],
        [InlineKeyboardButton(text="20 т", callback_data="tonnage_20")],
        [InlineKeyboardButton(text="24 т", callback_data="tonnage_24")],
    ]
)

# Старт FSM
@router.message(lambda msg: msg.text == "📦 Розрахувати вартість доставки")
async def start(message: Message, state: FSMContext):
    await message.answer("📍 Введіть точку А (місто/адреса):")
    await state.set_state(DeliveryForm.origin_city)

@router.message(DeliveryForm.origin_city)
async def set_origin(message: Message, state: FSMContext):
    await state.update_data(origin=message.text)
    await message.answer("🏁 Введіть точку Б (місто/адреса):")
    await state.set_state(DeliveryForm.destination_city)

@router.message(DeliveryForm.destination_city)
async def set_destination(message: Message, state: FSMContext):
    await state.update_data(destination=message.text)
    await message.answer("🚛 Оберіть тип автомобіля:", reply_markup=vehicle_kb)
    await state.set_state(DeliveryForm.cargo_type)

@router.callback_query(F.data.startswith("vehicle_"))
async def choose_vehicle(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    vehicle = callback.data.replace("vehicle_", "")
    await state.update_data(vehicle=vehicle)
    await callback.message.answer("⚖️ Оберіть тоннаж вантажу:", reply_markup=tonnage_kb)
    await state.set_state(DeliveryForm.weight)

@router.callback_query(F.data.startswith("tonnage_"))
async def choose_tonnage(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    tonnage = int(callback.data.replace("tonnage_", ""))
    await state.update_data(tonnage=tonnage)
    data = await state.get_data()

    fuel_price, fuel_date = await get_current_fuel_price()
    if fuel_price is None:
        fuel_price = 52.28
        fuel_date = "06.06.2025"

    # Отримуємо маршрут
    route = await get_route_data(data['origin'], data['destination'])
    if not route:
        await callback.message.answer("⚠️ Не вдалося побудувати маршрут. Перевірте введені адреси.")
        await state.clear()
        return

    distance_km = route['distance_km']
    duration_str = route['duration_str']
    polyline = route['polyline']

    # Розраховуємо вартість
    cost_data = calculate_cost(distance_km, data['vehicle'], fuel_price)

    # Створюємо зображення карти
    map_url = build_static_map(data['origin'], data['destination'], polyline)

    # Надсилаємо зображення
    await callback.message.answer_photo(photo=map_url)

    # Формуємо текст відповіді
    result_text = (
        f"*Маршрут*\n"
        f"{data['origin']} - {data['destination']}\n"
        f"{distance_km} км · {duration_str}\n"
        f"Вартість 1 км: {cost_data['per_km']} грн\n\n"
        f"*Транспортні витрати*\n"
        f"{cost_data['fuel_l']} л – розхід палива\n"
        f"{cost_data['fuel_price']} грн/л – ціна пального ({fuel_date})\n"
        f"{cost_data['fuel_cost']} грн – витрати на паливо\n\n"
        f"*Вартість*\n"
        f"{cost_data['total']} грн – вартість перевезення"
    )

    # Кнопка оформлення замовлення
    confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Оформити замовлення", callback_data="confirm_order")]
        ]
    )

    await callback.message.answer(result_text, parse_mode="Markdown", reply_markup=confirm_kb)
    await state.update_data(cost_data=cost_data, route_data=route)
    await state.set_state(DeliveryForm.confirmation)

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    full_data = await state.get_data()

    order_data = {
        "origin": full_data["origin"],
        "destination": full_data["destination"],
        "vehicle": full_data["vehicle"],
        "tonnage": full_data["tonnage"],
        "distance_km": full_data["route_data"]["distance_km"],
        "duration_str": full_data["route_data"]["duration_str"],
        "per_km": full_data["cost_data"]["per_km"],
        "fuel_l": full_data["cost_data"]["fuel_l"],
        "fuel_price": full_data["cost_data"]["fuel_price"],
        "fuel_cost": full_data["cost_data"]["fuel_cost"],
        "total": full_data["cost_data"]["total"],
    }

    save_order(user_id, order_data)
    await callback.message.answer("✅ Ваше замовлення оформлено.\nСтатус: *в обробці*", parse_mode="Markdown")
    await state.clear()

@router.message(lambda msg: msg.text == "🚛 Відстежити замовлення")
async def track_order(message: Message):
    orders = get_orders_by_user(message.from_user.id)

    if not orders:
        await message.answer("🔍 У вас ще немає активних замовлень.")
        return

    latest = orders[0]
    text = (
        f"📦 *Ваше останнє замовлення:*\n"
        f"🚚 Тип авто: {latest[4]}\n"
        f"⚖️ Вага: {latest[5]} т\n"
        f"📍 Маршрут: {latest[2]} → {latest[3]}\n"
        f"📏 Відстань: {latest[6]} км\n"
        f"🕓 Час доставки: {latest[7]}\n"
        f"💸 Вартість: {latest[12]} грн\n"
        f"📌 Статус: *{latest[13]}*\n"
        f"🕐 Дата: {latest[14]}"
    )
    await message.answer(text, parse_mode="Markdown")