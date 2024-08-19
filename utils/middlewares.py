import time

import config

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

from utils.keyboards import KB
from utils.repositories import UserRepository, SessionRepository


class SessionMiddleware(BaseMiddleware):

    def __init__(self, user_repo: UserRepository, session_repo: SessionRepository):
        self.user_repo = user_repo
        self.session_repo = session_repo

    async def _check_timeout_session(self, user_id) -> bool:
        session = await self.session_repo.get(user_id)
        res = time.time() - session.updated
        return True if res > config.MAX_SESSION_TIME_SECS else False

    async def session_middleware(self, event) -> bool:
        if await self.session_repo.get(event.from_user.id):
            if await self._check_timeout_session(event.from_user.id):
                await self.session_repo.update(event.from_user.id)
                return False
        else:
            user = await self.user_repo.get(event.from_user.id)
            if not user:
                await event.answer('Пользователь не найден',
                                   reply_markup=KB.back_to_main())
            await self.session_repo.add(user)
        return True

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id in self.user_repo.banned:
            return await event.answer("Ваш аккаунт заблокирован. Обратитесь в поддержку.")
        if not await self.session_middleware(event):
            if isinstance(event, Message):
                return await event.answer("Ваша сессия истекла, начните заново.",
                                          reply_markup=KB.back_to_main())
            if isinstance(event, CallbackQuery):
                return await event.message.edit_text("Ваша сессия истекла, начните заново.",
                                                     reply_markup=KB.back_to_main())
        return await handler(event, data)
