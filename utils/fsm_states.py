from aiogram.fsm.state import State, StatesGroup


class MyRequestsFSM(StatesGroup):
    delete_requests = State()
