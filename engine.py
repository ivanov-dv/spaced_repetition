import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

import config

from utils.db import AlchemySqlDb
from utils.middlewares import SessionMiddleware
from utils.models_orm import Base
from utils.repositories import UserRepository, SessionRepository, RequestRepository
from utils.service import Monitoring

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
middleware = SessionMiddleware(user_repo, session_repo)


'''
Monitoring
'''
monitoring = Monitoring(user_repo, request_repo, telegram_bot)
