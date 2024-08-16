from datetime import datetime
from uuid import UUID
from sqlalchemy import ForeignKey, BigInteger, Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from utils.models import User, UserRequest


class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    ban: Mapped[bool] = mapped_column(default=False)
    created: Mapped[datetime] = mapped_column()
    updated: Mapped[datetime] = mapped_column()
    requests: Mapped["UserRequestOrm"] = relationship(cascade="all, delete-orphan")

    @classmethod
    def from_model(cls, user: User):
        return cls(
            user_id=user.user_id,
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            ban=user.ban,
            created=user.created,
            updated=user.updated,
        )


class UserRequestOrm(Base):
    __tablename__ = "user_requests"

    request_id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column()
    ratio: Mapped[float] = mapped_column()
    count_day: Mapped[float] = mapped_column()
    date_notice = mapped_column(Date)
    created: Mapped[datetime] = mapped_column()
    updated: Mapped[datetime] = mapped_column()

    @classmethod
    def from_model(cls, request: UserRequest):
        return cls(
            request_id=request.request_id,
            user_id=request.user_id,
            text=request.text,
            ratio=request.ratio,
            count_day=request.count_day,
            date_notice=request.date_notice,
            created=request.created,
            updated=request.updated,
        )
