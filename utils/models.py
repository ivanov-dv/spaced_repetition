import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from time import time



@dataclass
class User:
    user_id: int
    firstname: str
    lastname: str
    username: str
    ban: bool
    created: datetime
    updated: datetime

    @classmethod
    def create(cls, user_id: int, firstname: str, lastname: str, username: str):
        dt = datetime.utcnow()
        return cls(user_id, firstname, lastname, username, False, dt, dt)

    @classmethod
    def from_orm(cls, user_orm):
        user_orm.__dict__.pop('_sa_instance_state')
        return cls(**user_orm.__dict__)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.user_id == other
        return self.user_id == other.user_id

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.user_id)


@dataclass
class UserRequest:
    request_id: uuid.UUID
    user_id: int
    text: str
    ratio: float
    count_day: float
    date_notice: datetime
    created: datetime
    updated: datetime

    @classmethod
    def create(cls, user_id,  text: str, ratio, count_day: int):
        dt = datetime.utcnow()
        td = timedelta(count_day)
        date_notice = dt + td
        return cls(uuid.uuid4(), user_id, text, ratio, count_day, date_notice.date(), dt, dt)

    @classmethod
    def from_orm(cls, request_orm):
        request_orm.__dict__.pop('_sa_instance_state')
        return cls(**request_orm.__dict__)

    async def calculate_next_date_notice(self, ratio: float = None):
        if ratio:
            self.ratio = ratio
        self.count_day = round(self.ratio * self.count_day + 1, 2)
        self.date_notice = self.date_notice + timedelta(int(self.count_day))

    def __str__(self):
        return (f'Задача: {self.text}\n'
                f'Уведомить: {self.date_notice.strftime("%d.%m.%Y")}\n'
                f'Создана: {self.created.date().strftime("%d.%m.%Y")}\n')


@dataclass
class Session:
    session_id: uuid.UUID
    created: time
    updated: time

    @classmethod
    def create(cls):
        session_id = uuid.uuid4()
        t = time()
        return cls(session_id, t, t)
