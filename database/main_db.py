import aiosqlite

from database.queries import (
    CREATE_PRODUCTS_TABLE,
    CREATE_PRODUCT_INFO_TABLE,
    INSERT_PRODUCT,
    INSERT_PRODUCT_INFO,
    SELECT_PRODUCTS,
    SELECT_PRODUCT_BY_ID,
    DELETE_PRODUCT,
    DELETE_PRODUCT_INFO
)


DB_NAME = "sqlite3.db"


# создание таблиц
async def create_table():

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            CREATE_PRODUCTS_TABLE
        )

        await db.execute(
            CREATE_PRODUCT_INFO_TABLE
        )

        await db.commit()



# добавление товара в первую таблицу
async def add_product(
        product_id,
        name,
        price
):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            INSERT_PRODUCT,
            (
                product_id,
                name,
                price
            )
        )

        await db.commit()



# добавление информации о товаре во вторую таблицу
async def add_product_info(
        product_id,
        category,
        description
):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            INSERT_PRODUCT_INFO,
            (
                product_id,
                category,
                description
            )
        )

        await db.commit()



# получение списка товаров через INNER JOIN
async def get_products():

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            SELECT_PRODUCTS
        )

        result = await cursor.fetchall()

        return result



# получение одного товара
async def get_product(product_id):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            SELECT_PRODUCT_BY_ID,
            (product_id,)
        )

        result = await cursor.fetchone()

        return result



# удаление товара из двух таблиц
async def delete_product(product_id):

    async with aiosqlite.connect(DB_NAME) as db:

        # удаляем дополнительную информацию
        await db.execute(
            DELETE_PRODUCT_INFO,
            (product_id,)
        )


        # удаляем сам товар
        await db.execute(
            DELETE_PRODUCT,
            (product_id,)
        )


        # один commit после двух запросов
        await db.commit()