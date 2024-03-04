from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    text_state = State()
    image_state = State()

class Buy(StatesGroup):
    chooce_amount = State()
    confirmation = State()

class Admin(StatesGroup):
    enter_id = State()
    enter_amount = State()
    confirm_token = State()
    enter_label = State()
    confirm_order = State()
    ban = State()