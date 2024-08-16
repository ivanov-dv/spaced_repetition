from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from engine import user_repo
from utils import texts
from utils.keyboards import KB
from utils.models import User

main_router = Router()


@main_router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    if await user_repo.get(message.from_user.id):
        await message.answer(f'🔆 Привет, {message.from_user.first_name}!\n\n'
                             f'👀 Давай посмотрим, что тут у нас...',
                             reply_markup=KB.main())
    else:
        user = User.create(message.from_user.id, message.from_user.first_name,
                           message.from_user.last_name, message.from_user.username)
        try:
            await user_repo.add(user)
        except Exception as e:
            await message.answer(f'Ошибка start: {e}', reply_markup=KB.main())


@main_router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if await user_repo.get(callback.from_user.id):
        await callback.message.edit_text(f'🔆 Привет, {callback.from_user.first_name}!\n\n'
                                         f'👀 Давай посмотрим, что тут у нас...',
                                         reply_markup=KB.main())
    else:
        user = User.create(callback.from_user.id, callback.from_user.first_name,
                           callback.from_user.last_name, callback.from_user.username)
        try:
            await user_repo.add(user)
        except Exception as e:
            await callback.message.edit_text(f'Ошибка start_callback: {e}', reply_markup=KB.main())


@main_router.callback_query(F.data == 'description')
async def description(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(texts.main(), reply_markup=KB.back_to_main())


@main_router.callback_query(F.data == 'remove_notice')
async def remove_notice(callback: types.CallbackQuery):
    await callback.message.delete()
