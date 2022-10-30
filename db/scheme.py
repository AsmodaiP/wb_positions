
from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    favorite_queries = relationship("FavoriteQueries", back_populates="telegram_user")

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r}, chat_id={0.telegram_id!r})>".format(self)


class FavoriteQueries(BaseModel):
    __tablename__ = 'favorite_queries'

    telegram_user_id = Column(Integer, ForeignKey('telegram_users.id'))
    telegram_user = relationship("TelegramUser", back_populates="favorite_queries")
    query = relationship("UserQueries")
    query_id = Column(Integer, ForeignKey('user_queries.id'))

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r}, query={0.query!r})>".format(self)


class UserQueries(BaseModel):
    __tablename__ = 'user_queries'

    telegram_user_id = Column(Integer, ForeignKey('telegram_users.id'), nullable=False)
    telegram_user = relationship("TelegramUser", back_populates="user_queries")
    article = Column(Integer, nullable=False)
    query = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    dst = Column(String, nullable=False)
    position = Column(Integer, nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r}, query={0.query!r})>".format(self)


class PickUps(BaseModel):
    __tablename__ = 'pickups'

    address = Column(String(255), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    wb_dst = Column(String(255), nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r}, address={0.address!r})>".format(self)
