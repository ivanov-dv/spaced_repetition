import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

import config

from utils.db import AlchemySqlDb
from utils.models_orm import Base
from utils.repositories import UserRepository, SessionRepository, RequestRepository

'''
Database
'''
db = AlchemySqlDb(config.SQLALCHEMY_DATABASE_URL, Base)

'''
Repositories
'''
user_repo = UserRepository(db)
request_repo = RequestRepository(db)
session_repo = SessionRepository()


'''
Telegram API
'''
telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=config.TELEGRAM_PARSE_MODE))
logging.basicConfig(level=config.LOG_LEVEL, stream=sys.stdout)


# import asyncio
# from utils.models import *
# r1 = UserRequest.create(334984636, 'test1', 0)
# r2 = UserRequest.create(334984636, 'test2', 4)
# r3 = UserRequest.create(334984636, 'test3', 12)
#
#
# async def main():
#     await request_repo.db.prepare()
#     await request_repo.add(r1)
#     await request_repo.add(r2)
#     await request_repo.add(r3)
#
# asyncio.run(main())
