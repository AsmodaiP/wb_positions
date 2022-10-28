import datetime
from stat import FILE_ATTRIBUTE_ARCHIVE
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, TIMESTAMP, Float, Date
from sqlalchemy.orm import mapper, sessionmaker, relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class TelegramUser(BaseModel):
    __tablename__ = 'telegram_users'

    chat_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    user_queries = relationship("UserQueries", back_populates="telegram_user")

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r}, chat_id={0.telegram_id!r})>".format(self)


class UserQueries(BaseModel):
    __tablename__ = 'users_articles'

    telegram_user_id = Column(Integer, ForeignKey('telegram_users.id'), nullable=False)
    telegram_user = relationship("TelegramUser", back_populates="user_queries")
    article = Column(Integer, nullable=False)
    query = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r}, telegram_user_id={0.telegram_user_id!r}, article_id={0.article_id!r})>".format(self)


class Positions(BaseModel):
    __tablename__ = 'positions'

    article = Column(Integer, nullable=False)
    query = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)


class PickUps(BaseModel):
    __tablename__ = 'pickups'

    address = Column(String(255), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    wb_dst = Column(String(255), nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r}, address={0.address!r})>".format(self)
