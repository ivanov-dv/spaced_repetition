from aiogram.fsm.state import State, StatesGroup


class CreateRequestFSM(StatesGroup):
    get_ratio = State()
    get_text = State()
    get_count_day = State()


class MyRequestsFSM(StatesGroup):
    delete_requests = State()
