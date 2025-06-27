from aiogram.fsm.state import StatesGroup, State


class TaskDialogSG(StatesGroup):
    menu = State()
    tasks = State()
    add_title = State()
    add_due_date = State()
    finish = State()
