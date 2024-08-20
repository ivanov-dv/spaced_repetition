import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot

from utils.keyboards import KB
from utils.repositories import UserRepository, RequestRepository


class Monitoring:
    def __init__(self, user_repo: UserRepository, request_repo: RequestRepository, bot: Bot):
        self.user_repo = user_repo
        self.request_repo = request_repo
        self.bot = bot
        self.count = 0

    async def check(self):
        while True:
            self.count += 1
            print('Цикл: ', self.count)
            user_requests = await self.request_repo.get_all_requests()
            for request in user_requests:
                if request.date_notice <= datetime.utcnow().date():
                    if datetime.utcnow().hour >= 9:
                        await request.calculate_next_date_notice()
                        try:
                            await self.bot.send_message(
                                request.user_id,
                                f'🔊 Повторить 📖:\n\n'
                                f'{request.text}\n\n'
                                f'Следующее напоминание: {request.date_notice.strftime("%d.%m.%Y")}',
                                reply_markup=KB.remove_notice())
                        except Exception as e:
                            print(f'Ошибка отправки уведомления для пользователя {request.user_id}: {str(e)}')
                            logging.error(f'Ошибка отправки уведомления для пользователя {request.user_id}: {str(e)}')
                            continue
                        else:
                            await self.request_repo.update(request)
            await asyncio.sleep(60*60*6)
