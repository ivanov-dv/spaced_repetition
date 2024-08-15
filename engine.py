import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import config

from utils.db import AlchemySqlDb
from utils.middlewares import SessionMiddleware
from utils.models_orm import Base
from utils.repositories import UserRepository, SessionRepository


'''
Database
'''
db = AlchemySqlDb(config.SQLALCHEMY_DATABASE_URL, Base)

'''
Repositories
'''
user_repo = UserRepository(db)
session_repo = SessionRepository()


'''
Telegram API
'''
telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=config.TELEGRAM_PARSE_MODE))
logging.basicConfig(level=config.LOG_LEVEL, stream=sys.stdout)

