from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    text_state = State()
    image_state = State()