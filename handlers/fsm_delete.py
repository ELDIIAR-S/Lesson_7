from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.main_db import delete_product

from handlers.buttons import delete_confirm_keyboard


router = Router()


# состояние подтверждения удаления
class DeleteState(StatesGroup):

    confirm = State()



# 1. нажали 🗑 Удалить -> спрашиваем подтверждение

@router.callback_query(F.data.startswith("delete:"))
async def delete_start(
        call: CallbackQuery,
        state: FSMContext
):

    # callback_data вида "delete:1001" -> достаём артикул
    product_id = call.data.split(":")[1]

    await state.update_data(
        product_id=product_id
    )

    await state.set_state(
        DeleteState.confirm
    )

    await call.message.answer(
        f"Точно удалить товар с артикулом {product_id}?",
        reply_markup=delete_confirm_keyboard
    )

    await call.answer()



# 2. подтвердили удаление

@router.callback_query(
    DeleteState.confirm,
    F.data == "delete_yes"
)
async def delete_confirm(
        call: CallbackQuery,
        state: FSMContext
):

    data = await state.get_data()

    product_id = data["product_id"]

    await delete_product(product_id)

    await call.message.answer(
        f"Товар с артикулом {product_id} удалён"
    )

    await call.answer()

    await state.clear()



# 3. отменили удаление

@router.callback_query(
    DeleteState.confirm,
    F.data == "delete_no"
)
async def delete_cancel(
        call: CallbackQuery,
        state: FSMContext
):

    await call.message.answer(
        "Удаление отменено"
    )

    await call.answer()

    await state.clear()