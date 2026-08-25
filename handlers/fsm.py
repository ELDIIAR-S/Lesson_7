from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.main_db import (
    add_product_db,
    add_product_info_db,
    get_products
)

from handlers.buttons import product_card_keyboard


router = Router()


# /start

@router.message(Command("start"))
async def start_command(message: Message):

    await message.answer(
        "Привет!\n\n"
        "Команды:\n"
        "/add_product — добавить товар\n"
        "/products — посмотреть товары"
    )



# FSM добавление товара

class ProductState(StatesGroup):

    article = State()
    name = State()
    price = State()
    category = State()
    description = State()



# начало добавления

@router.message(Command("add_product"))
async def add_product_start(
        message: Message,
        state: FSMContext
):

    await message.answer(
        "Введите артикул товара:"
    )

    await state.set_state(
        ProductState.article
    )



# артикул

@router.message(ProductState.article)
async def product_article(
        message: Message,
        state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Артикул должен быть числом"
        )

        return

    await state.update_data(
        article=int(message.text)
    )

    await message.answer(
        "Введите название товара:"
    )

    await state.set_state(
        ProductState.name
    )



# название

@router.message(ProductState.name)
async def product_name(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        name=message.text
    )

    await message.answer(
        "Введите цену товара:"
    )

    await state.set_state(
        ProductState.price
    )



# цена

@router.message(ProductState.price)
async def product_price(
        message: Message,
        state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Цена должна быть числом"
        )

        return

    await state.update_data(
        price=int(message.text)
    )

    await message.answer(
        "Введите категорию товара:"
    )

    await state.set_state(
        ProductState.category
    )



# категория

@router.message(ProductState.category)
async def product_category(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        category=message.text
    )

    await message.answer(
        "Введите описание товара:"
    )

    await state.set_state(
        ProductState.description
    )



# описание + сохранение

@router.message(ProductState.description)
async def product_description(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        description=message.text
    )

    data = await state.get_data()

    # первая таблица products
    await add_product_db(
        data["article"],
        data["name"],
        data["price"]
    )

    # вторая таблица product_info
    await add_product_info_db(
        data["article"],
        data["category"],
        data["description"]
    )

    await message.answer(
        "Товар успешно добавлен"
    )

    await state.clear()



# Список товаров — каждый товар отдельной карточкой с кнопкой удаления

@router.message(Command("products"))
async def products_command(
        message: Message
):

    products = await get_products()

    if not products:

        await message.answer(
            "Товаров пока нет"
        )

        return

    for product in products:

        product_id = product[0]

        text = (
            f"Артикул: {product[0]}\n"
            f"Название: {product[1]}\n"
            f"Цена: {product[2]}\n"
            f"Категория: {product[3]}\n"
            f"Описание: {product[4]}"
        )

        await message.answer(
            text,
            reply_markup=product_card_keyboard(product_id)
        )
        
# from aiogram import Router
# from aiogram.types import Message
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State


# from database.main_db import (
#     add_product,
#     add_product_info,
#     get_products
# )


# router = Router()


# # /start

# @router.message(Command("start"))
# async def start_command(message: Message):

#     await message.answer(
#         "Привет!\n\n"
#         "Команды:\n"
#         "/add_product — добавить товар\n"
#         "/products — посмотреть товары"
#     )



# # FSM добавление товара

# class ProductState(StatesGroup):

#     article = State()
#     name = State()
#     price = State()
#     category = State()
#     description = State()



# # начало добавления

# @router.message(Command("add_product"))
# async def add_product_start(
#         message: Message,
#         state: FSMContext
# ):

#     await message.answer(
#         "Введите артикул товара:"
#     )

#     await state.set_state(
#         ProductState.article
#     )



# # артикул

# @router.message(ProductState.article)
# async def product_article(
#         message: Message,
#         state: FSMContext
# ):

#     await state.update_data(
#         article=message.text
#     )


#     await message.answer(
#         "Введите название товара:"
#     )


#     await state.set_state(
#         ProductState.name
#     )



# # название

# @router.message(ProductState.name)
# async def product_name(
#         message: Message,
#         state: FSMContext
# ):

#     await state.update_data(
#         name=message.text
#     )


#     await message.answer(
#         "Введите цену товара:"
#     )


#     await state.set_state(
#         ProductState.price
#     )



# # цена

# @router.message(ProductState.price)
# async def product_price(
#         message: Message,
#         state: FSMContext
# ):

#     if not message.text.isdigit():

#         await message.answer(
#             "Цена должна быть числом"
#         )

#         return


#     await state.update_data(
#         price=int(message.text)
#     )


#     await message.answer(
#         "Введите категорию товара:"
#     )


#     await state.set_state(
#         ProductState.category
#     )



# # категория

# @router.message(ProductState.category)
# async def product_category(
#         message: Message,
#         state: FSMContext
# ):

#     await state.update_data(
#         category=message.text
#     )


#     await message.answer(
#         "Введите описание товара:"
#     )


#     await state.set_state(
#         ProductState.description
#     )



# # описание + сохранение

# @router.message(ProductState.description)
# async def product_description(
#         message: Message,
#         state: FSMContext
# ):

#     await state.update_data(
#         description=message.text
#     )


#     data = await state.get_data()


#     # первая таблица products
#     await add_product(
#         data["article"],
#         data["name"],
#         data["price"]
#     )


#     # вторая таблица product_info
#     await add_product_info(
#         data["article"],
#         data["category"],
#         data["description"]
#     )


#     await message.answer(
#         "Товар успешно добавлен"
#     )


#     await state.clear()



# # Список товаров INNER JOIN

# @router.message(Command("products"))
# async def products_command(
#         message: Message
# ):

#     products = await get_products()


#     if not products:

#         await message.answer(
#             "Товаров пока нет"
#         )

#         return


#     text = "Список товаров:\n\n"


#     for product in products:

#         text += (
#             f"Артикул: {product[0]}\n"
#             f"Название: {product[1]}\n"
#             f"Цена: {product[2]}\n"
#             f"Категория: {product[3]}\n"
#             f"Описание: {product[4]}\n\n"
#         )


#     await message.answer(text)