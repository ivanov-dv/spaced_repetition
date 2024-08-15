from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class KB:
    b_back_to_main = InlineKeyboardButton(text='На главную', callback_data='start')
    b_create_notice = InlineKeyboardButton(text='Создать уведомление', callback_data='create_notice')
    b_my_notices = InlineKeyboardButton(text='Мои уведомления', callback_data='my_notices')
    b_remove_notice = InlineKeyboardButton(text='Удалить', callback_data='remove_notice')

    @classmethod
    def main(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_create_notice, cls.b_my_notices)
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
