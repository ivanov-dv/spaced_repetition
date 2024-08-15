from datetime import datetime
from sqlalchemy import select, update, delete
from time import time

from utils.db import AlchemySqlDb
from utils.models import User, Session
from utils.models_orm import UserOrm


class RepositoryDb:
    def __init__(self, db: AlchemySqlDb):
        self.db = db


class UserRepository(RepositoryDb):
    banned: set = set()

    async def add(self, user: User) -> User:
        async with self.db.SessionLocal() as session:
            user_orm = UserOrm.from_model(user)
            session.add(user_orm)
            await session.commit()
            return user

    async def get(self, user_id: int) -> User | None:
        async with self.db.SessionLocal() as session:
            res = await session.execute(select(UserOrm).where(UserOrm.user_id == user_id))
            user_orm = res.scalar_one_or_none()
            return User.from_orm(user_orm) if user_orm else None

    async def update(self, user: User) -> User:
        async with self.db.SessionLocal() as session:
            user.updated = datetime.utcnow()
            await session.execute(
                update(UserOrm)
                .values(
                    firstname=user.firstname,
                    lastname=user.lastname,
                    username=user.username,
                    ban=user.ban,
                    updated=user.updated,
                )
                .where(UserOrm.user_id == user.user_id)
            )
            await session.commit()
            return user

    async def delete(self, user_id: int) -> None:
        async with self.db.SessionLocal() as session:
            await session.execute(delete(UserOrm).where(UserOrm.user_id == user_id))
            await session.commit()

    async def load_from_db(self):
        async with self.db.SessionLocal() as session:
            res = await session.execute(select(UserOrm).where(UserOrm.ban is True))
            for user_orm in res:
                self.banned.add(user_orm.user_id)


class SessionRepository:
    sessions: dict[User, Session] = {}

    async def add(self, user: User, session: Session) -> Session:
        self.sessions.update({user: session})
        return session

    async def get(self, user_id: int) -> Session | None:
        return self.sessions.get(user_id)

    async def update(self, user_id: int) -> Session | None:
        session = self.sessions.get(user_id)
        if not session:
            return
        session.updated = time()
        self.sessions.update({user_id: session})
        return session

    async def delete(self, user_id: int) -> None:
        self.sessions.pop(user_id, None)
