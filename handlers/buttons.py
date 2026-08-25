from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


delete_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да, удалить",
                callback_data="delete_yes"
            )
        ],
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="delete_no"
            )
        ]
    ]
)