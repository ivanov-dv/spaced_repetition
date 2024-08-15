from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.keyboards import KB


router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Привет {message.from_user.first_name}', reply_markup=KB.main())


@router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(f'Привет {callback.from_user.first_name}', reply_markup=KB.main())
