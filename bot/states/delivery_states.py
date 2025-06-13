from aiogram.fsm.state import State, StatesGroup

class DeliveryForm(StatesGroup):
    origin_city = State()
    destination_city = State()
    cargo_type = State()
    weight = State()
    confirmation = State()