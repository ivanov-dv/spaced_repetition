import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from engine import telegram_bot, user_repo, session_repo, monitoring
from handlers import main_handlers, my_requests, create_request
from utils.middlewares import SessionMiddleware


async def main_bot():
    dp = Dispatcher(storage=MemoryStorage())
    middleware = SessionMiddleware(user_repo, session_repo)
    create_request.router.message.outer_middleware(middleware)
    create_request.router.callback_query.outer_middleware(middleware)
    dp.include_routers(
        main_handlers.main_router,
        my_requests.router,
        create_request.router
    )
    await user_repo.db.prepare()
    await user_repo.load_from_db()
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


async def main():
    await asyncio.gather(
        main_bot(),
        monitoring.check()
    )


if __name__ == "__main__":
    asyncio.run(main())
