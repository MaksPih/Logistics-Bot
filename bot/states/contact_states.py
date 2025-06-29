from aiogram.fsm.state import StatesGroup, State

class ContactForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_comment = State()