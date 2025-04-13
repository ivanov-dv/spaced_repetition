import asyncio

import sentry_sdk
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import SENTRY_DSN
from engine import telegram_bot, user_repo, monitoring
from handlers import main_handlers, my_requests, create_request


async def main_bot():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        main_handlers.main_router,
        my_requests.router,
        create_request.router,
        create_request.check_session
    )
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


async def main():
    await user_repo.db.prepare()
    await user_repo.load_from_db()
    await asyncio.gather(
        main_bot(),
        monitoring.check()
    )


if __name__ == "__main__":
    if SENTRY_DSN:
        sentry_sdk.init(SENTRY_DSN)
    asyncio.run(main())
