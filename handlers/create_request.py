from aiogram import types, F, Router, exceptions
from aiogram.fsm.context import FSMContext

from engine import middleware, request_repo
from utils import texts, assist
from utils.fsm_states import CreateRequestFSM
from utils.keyboards import KB, CreateRequestKb
from utils.models import UserRequest

router = Router()

router.message.middleware(middleware)
router.callback_query.middleware(middleware)


@router.callback_query(F.data == 'cr_my_ratio')
async def ask_my_ratio(callback: types.CallbackQuery):
    await callback.message.edit_text('⌨️ Введите коэффициент частоты повторений R от 1 до 5:\n\n👇 ⌨️',
                                     reply_markup=KB.back_to_main())


@router.message(CreateRequestFSM.get_ratio)
async def get_my_ratio(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    ratio = assist.validate_my_ratio(message.text)
    msg = data['msg']
    if not ratio:
        try:
            await msg.edit_text(f'{texts.incorrect_value()}\n\n'
                                'В⌨️ Введите коэффициент частоты повторений R от 1 до 5:\n\n👇 ⌨️',
                                reply_markup=CreateRequestKb.back_to_main())
        except exceptions.TelegramBadRequest:
            try:
                await msg.answer()
            except TypeError:
                pass
    else:
        msg = await data['msg'].edit_text(texts.get_text(), reply_markup=KB.back_to_main())
        await state.update_data({'ratio': ratio, 'msg': msg})
        await state.set_state(CreateRequestFSM.get_text)


@router.callback_query(F.data == 'cr_ratio_2_5')
async def choose_ratio_2_5(callback: types.CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(texts.get_text(), reply_markup=KB.back_to_main())
    await state.update_data({'ratio': 2.5, 'msg': msg})
    await state.set_state(CreateRequestFSM.get_text)


@router.callback_query(F.data == 'cr_ratio_2')
async def choose_ratio_2(callback: types.CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(texts.get_text(), reply_markup=KB.back_to_main())
    await state.update_data({'ratio': 2, 'msg': msg})
    await state.set_state(CreateRequestFSM.get_text)


@router.message(CreateRequestFSM.get_text)
async def get_text(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    text = assist.validate_text(message.text)
    ratio = data['ratio']
    msg = data['msg']
    if not text:
        await msg.edit_text(f'{texts.incorrect_value()}\n\n'
                            f'{texts.get_text()}',
                            reply_markup=KB.back_to_main())
    else:
        if data['ratio'] == 2 or data['ratio'] == 2.5:
            request = UserRequest.create(message.from_user.id, text, ratio, 1)
            try:
                await request_repo.add(request)
            except Exception as e:
                await msg.edit_text(f'Ошибка создания запроса в БД: {str(e)}', reply_markup=KB.back_to_main())
            await msg.edit_text('✅ Задача успешно создана!\n\n'
                                f'{request}',
                                reply_markup=KB.main())
        else:
            await msg.edit_text(texts.get_count_day(ratio),
                                reply_markup=KB.back_to_main())
            await state.update_data({'text': text, 'msg': msg})
            await state.set_state(CreateRequestFSM.get_count_day)


@router.message(CreateRequestFSM.get_count_day)
async def get_count_day(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    count_day = assist.validate_count_day(message.text)
    text = data['text']
    ratio = data['ratio']
    msg = data['msg']
    if count_day is False:
        await msg.edit_text(f'{texts.incorrect_value()}\n\n'
                            f'{texts.get_count_day(ratio)}',
                            reply_markup=KB.back_to_main())
    else:
        request = UserRequest.create(message.from_user.id, text, ratio, count_day)
        try:
            await request_repo.add(request)
        except Exception as e:
            await msg.edit_text(f'Ошибка создания запроса в БД: {str(e)}', reply_markup=KB.back_to_main())
        await msg.edit_text('✅ Задача успешно создана!\n\n'
                            f'{request}',
                            reply_markup=KB.main())
