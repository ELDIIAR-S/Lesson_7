import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database.main_db import create_table

from handlers.fsm import router as fsm_router
from handlers.fsm_delete import router as delete_router


async def main():

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()


    # подключаем хендлеры
    dp.include_router(fsm_router)

    # роутер удаления товара
    dp.include_router(delete_router)


    # создаём таблицы при запуске
    await create_table()


    # запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())