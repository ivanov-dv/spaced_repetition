import pytest

from datetime import datetime

import utils.assist as assist

from utils.models import User, UserRequest, Session
from utils.repositories import SessionRepository


class TestRequest:
    dt = datetime(2000, 5, 20)

    ur1 = UserRequest.create('test', 1, 0)
    ur1.date_notice = dt
    ur2 = UserRequest.create('test', 2, 5)
    ur2.date_notice = dt

    @pytest.mark.asyncio
    async def test_calculate(self):
        assert self.ur1.count_day == 0
        assert self.ur2.count_day == 5

        await self.ur1.calculate_next_date_notice(2)
        await self.ur2.calculate_next_date_notice(2)
        assert self.ur1.count_day == 1
        assert self.ur1.date_notice.day == 21
        assert self.ur2.count_day == 11
        assert self.ur2.date_notice.day == 31

        await self.ur1.calculate_next_date_notice(2)
        await self.ur2.calculate_next_date_notice(2)
        assert self.ur1.count_day == 3
        assert self.ur2.count_day == 23

        await self.ur1.calculate_next_date_notice(2.5)
        await self.ur2.calculate_next_date_notice(2.5)
        assert self.ur1.count_day == 8.5
        assert self.ur1.date_notice.day == 1
        assert self.ur2.count_day == 58.5
        assert self.ur2.date_notice.day == 20


class TestSessionRepository:
    session_repo = SessionRepository()
    user1 = User.create(1, 'Petr', 'Ivanov', 'petr_ivanov')
    user2 = User.create(2, 'Vasiliy', 'Petrov', 'vasiliy_petrov')
    session1 = Session.create()
    session2 = Session.create()

    @pytest.mark.asyncio
    async def test_add_session(self):
        await self.session_repo.add(self.user1, self.session1)
        await self.session_repo.add(self.user2, self.session2)
        assert len(self.session_repo.sessions) == 2

    @pytest.mark.asyncio
    async def test_get_session(self):
        session = await self.session_repo.get(1)
        assert session == self.session1

    @pytest.mark.asyncio
    async def test_update_session(self):
        session_old = self.session1.updated
        session = await self.session_repo.get(1)
        assert session.updated == self.session1.updated
        session = await self.session_repo.update(1)
        assert session.updated != session_old

    @pytest.mark.asyncio
    async def test_delete_session(self):
        await self.session_repo.delete(1)
        await self.session_repo.delete(2)
        assert self.session_repo.sessions == {}


class TestAssist:
    @staticmethod
    def test_validate_nums_requests():
        assert assist.validate_nums_requests(' 3, 2, 1, 2, 3,  5   ') == [1, 2, 3, 5]
        assert assist.validate_nums_requests('4') == [4]
        assert assist.validate_nums_requests('1 2 3, 4') is False
        assert assist.validate_nums_requests('1 2 3 a 4') is False
