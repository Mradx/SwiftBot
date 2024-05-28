from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    save_history = State()
    delete_history = State()
    update_instruction = State()
    update_last_response = State()
    update_language = State()
