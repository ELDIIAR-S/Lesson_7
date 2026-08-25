from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# клавиатура под карточкой товара
def product_card_keyboard(product_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"delete:{product_id}"
                )
            ]
        ]
    )



# клавиатура подтверждения удаления
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