import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from engine import telegram_bot, user_repo, session_repo
from handlers import main_handlers, my_requests
from utils.middlewares import SessionMiddleware


async def main_bot():
    dp = Dispatcher(storage=MemoryStorage())
    outer_middleware = SessionMiddleware(user_repo, session_repo)
    dp.message.outer_middleware(outer_middleware)
    dp.callback_query.outer_middleware(outer_middleware)
    dp.include_routers(
        main_handlers.main_router,
        my_requests.router,
    )
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main_bot())
