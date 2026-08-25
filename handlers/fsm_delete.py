from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from database.main_db import delete_product
from handlers.buttons import delete_confirm_keyboard


router = Router()



class DeleteState(StatesGroup):

    waiting_confirm = State()



# Нажали 🗑 Удалить
@router.callback_query(
    F.data.startswith("delete:")
)
async def delete_start(
        call: CallbackQuery,
        state: FSMContext
):

    product_id = call.data.split(":")[1]


    await state.update_data(
        product_id=product_id
    )


    await state.set_state(
        DeleteState.waiting_confirm
    )


    await call.message.answer(
        "Вы точно хотите удалить товар?",
        reply_markup=delete_confirm_keyboard
    )


    await call.answer()



# Нажали "Да, удалить"
@router.callback_query(
    DeleteState.waiting_confirm,
    F.data == "delete_yes"
)
async def delete_yes(
        call: CallbackQuery,
        state: FSMContext
):

    data = await state.get_data()


    product_id = data["product_id"]


    await delete_product(product_id)


    await call.message.answer(
        "Товар успешно удалён"
    )


    await state.clear()


    await call.answer()



# Нажали "Отмена"
@router.callback_query(
    DeleteState.waiting_confirm,
    F.data == "delete_no"
)
async def delete_no(
        call: CallbackQuery,
        state: FSMContext
):

    await call.message.answer(
        " Удаление отменено"
    )


    await state.clear()


    await call.answer()