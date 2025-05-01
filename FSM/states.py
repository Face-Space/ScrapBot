from aiogram.fsm.state import StatesGroup, State


class NextStep(StatesGroup):
    choose_category = State()
    set_filter = State()

