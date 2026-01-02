from aiogram.fsm.state import State, StatesGroup

class BuildState(StatesGroup):
    menu = State()
    choosing = State()
