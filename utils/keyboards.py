from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class KB:
    b_back_to_main = InlineKeyboardButton(text='На главную', callback_data='start')
    b_create_notice = InlineKeyboardButton(text='Создать уведомление', callback_data='create_request')
    b_my_requests = InlineKeyboardButton(text='Мои уведомления', callback_data='my_requests')
    b_remove_notice = InlineKeyboardButton(text='Удалить', callback_data='remove_notice')

    @classmethod
    def main(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_create_notice, cls.b_my_requests)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_main(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_main)
        return builder.as_markup()

    @classmethod
    def remove_notice(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_remove_notice)
        return builder.as_markup()


class CreateRequestKb(KB):
    b_ratio_2_5 = InlineKeyboardButton(
        text='Стандарт (R=2.5)', callback_data='cr_ratio_2_5'
    )
    b_ratio_2 = InlineKeyboardButton(
        text='Более часто (R=2)', callback_data='cr_ratio_2'
    )
    b_my_ratio = InlineKeyboardButton(
        text='Ввести вручную', callback_data='cr_my_ratio'
    )

    @classmethod
    def choose_ratio(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_ratio_2_5, cls.b_ratio_2, cls.b_my_ratio, cls.b_back_to_main)
        return builder.adjust(1).as_markup()


class MyRequestKb(KB):
    b_delete = InlineKeyboardButton(
        text='Выбрать и удалить', callback_data='mr_delete')
    b_delete_all = InlineKeyboardButton(
        text='Удалить все', callback_data='mr_delete_all')
    b_back_to_my_requests = InlineKeyboardButton(
        text='В мои уведомления', callback_data='my_requests')

    @classmethod
    def my_requests(cls):
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_delete,
            cls.b_delete_all,
            cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_my_requests(cls):
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_back_to_my_requests)
        return builder.as_markup()
