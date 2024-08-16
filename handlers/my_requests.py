import logging

from aiogram import types, F, Router, exceptions
from aiogram.fsm.context import FSMContext

from engine import request_repo
from utils import assist
from utils.fsm_states import MyRequestsFSM
from utils.keyboards import KB, MyRequestKb

router = Router()


@router.callback_query(F.data == 'my_requests')
async def show_my_requests(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user_requests = await request_repo.get_requests_for_user(callback.from_user.id)
    await state.set_data({'user_requests': user_requests})
    if not user_requests:
        try:
            await callback.message.edit_text('Не создано ни одной задачи.', reply_markup=KB.main())
        except exceptions.TelegramBadRequest:
            await callback.answer('Не создано ни одной задачи.')
    else:
        await callback.message.edit_text(assist.list_requests_to_text(user_requests),
                                         reply_markup=MyRequestKb.my_requests())


@router.callback_query(F.data == 'mr_delete')
async def ask_nums_for_delete_request(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_requests = data["user_requests"]
    msg = await callback.message.edit_text(f'{assist.list_requests_to_text(user_requests)}\n\n'
                                           f'⌨️ Введите номер или номера задач через запятую для удаления.\n'
                                           f'Например "2" или "2,4,6".\n\n👇 ⌨️',
                                           reply_markup=MyRequestKb.back_to_my_requests())
    await state.set_state(MyRequestsFSM.delete_requests)
    await state.set_data({'msg': msg, 'user_requests': user_requests})


@router.message(MyRequestsFSM.delete_requests)
async def delete_request(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    user_requests = data['user_requests']
    msg = data['msg']
    request_nums = assist.validate_nums_requests(message.text)
    if not request_nums:
        await msg.edit_text(f'<code>❗️ {"Некорректные значения":^25} ❗️\n'
                            f'❗️ {"Попробуйте заново":^25} ❗️</code>',
                            reply_markup=KB.main())
    flag = False
    for num in request_nums:
        request = user_requests[num - 1]
        try:
            await request_repo.delete(request.request_id)
        except Exception as e:
            logging.error(f'Ошибка удаления {request}: {str(e)}')
            flag = True
    if flag:
        await msg.edit_text('❗️ Ошибка. Не все задачи были удалены ❗️', reply_markup=KB.main())
    await msg.edit_text(f'✅ Задачи № [{", ".join(map(str, request_nums))}] удалены.', reply_markup=KB.main())


@router.callback_query(F.data == 'mr_delete_all')
async def delete_all_requests(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('⁉️ Вы уверены, что хотите удалить все напоминания?',
                                     reply_markup=MyRequestKb.delete_all_confirm())


@router.callback_query(F.data == 'mr_delete_all_confirm')
async def delete_all_requests_confirm(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_requests = data['user_requests']
    flag = False
    for request in user_requests:
        try:
            await request_repo.delete(request.request_id)
        except Exception as e:
            logging.error(f'Ошибка удаления {request}: {str(e)}')
            flag = True
    if flag:
        await callback.message.edit_text('❗️ Ошибка. Не все задачи были удалены ❗️', reply_markup=KB.main())
    await callback.message.edit_text('✅ Все задачи удалены.', reply_markup=KB.main())
