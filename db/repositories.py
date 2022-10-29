import datetime

from db.db import session
from db.scheme import FavoriteQueries, PickUps, TelegramUser, UserQueries
from utils.get_dst import get_coordinate_by_address, get_dst


class BaseRepository:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        raise NotImplementedError

    def get(self, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self, **kwargs):
        raise NotImplementedError


class TelegramUserRepository(BaseRepository):
    def create(self, chat_id, username, first_name, last_name):
        if self.get(chat_id):
            return self.update(chat_id, username=username, first_name=first_name, last_name=last_name)
        date = datetime.datetime.now()
        user = TelegramUser(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            created_at=date,
            updated_at=date,
        )
        self.session.add(user)
        return user

    def get(self, chat_id):
        return self.session.query(TelegramUser).filter_by(chat_id=chat_id).first()

    def update(self, chat_id, **kwargs):
        user = self.get(chat_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        return user

    def delete(self, chat_id):
        user = self.get(chat_id)
        self.session.delete(user)
        return user

    def commit(self):
        self.session.commit()


class PickUpsRepository(BaseRepository):
    def create(self, address, latitude, longitude, wb_dst):
        pickup = PickUps(
            address=address,
            latitude=latitude,
            longitude=longitude,
            wb_dst=wb_dst,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        self.session.add(pickup)
        return pickup

    def get_by_address(self, address) -> PickUps:
        pickup = self.session.query(PickUps).filter_by(address=address).first()
        if not pickup:
            return
        return pickup

    def create_by_address(self, address) -> PickUps:
        coordinate = get_coordinate_by_address(address)
        latitude = coordinate['latitude']
        longitude = coordinate['longitude']
        wb_dst = get_dst(address, longitude, latitude)
        return self.create(address, latitude, longitude, ','.join(wb_dst))

    def get(self, address):
        return self.session.query(PickUps).filter_by(address=address).first()

    def update(self, address, **kwargs):
        pickup = self.get(address)
        for key, value in kwargs.items():
            setattr(pickup, key, value)
        return pickup

    def delete(self, address):
        pickup = self.get(address)
        self.session.delete(pickup)
        return pickup

    def commit(self):
        self.session.commit()


class UserQueriesRepository(BaseRepository):
    def create(self, user_id, query, article, address, position):
        date = datetime.datetime.now()

        user_query = UserQueries(
            telegram_user_id=user_id,
            article=article,
            query=query,
            address=address,
            position=position,
            created_at=date,
            updated_at=date,
        )
        self.session.add(user_query)
        return user_query

    def get(self, user_id):
        return self.session.query(UserQueries).filter_by(user_id=user_id).first()

    def update(self, user_id, **kwargs):
        user_query = self.get(user_id)
        for key, value in kwargs.items():
            setattr(user_query, key, value)
        return user_query

    def delete(self, user_id):
        user_query = self.get(user_id)
        self.session.delete(user_query)
        return user_query

    def commit(self):
        self.session.commit()


class FavoriteQueriesRepository(BaseRepository):
    def create(self, user_id, query, article, address=None):
        date = datetime.datetime.now()

        favorite_query = FavoriteQueries(
            telegram_user_id=user_id,
            article=article,
            query=query,
            created_at=date,
            updated_at=date,
        )
        self.session.add(favorite_query)
        return favorite_query

    def get(self, user_id):
        return self.session.query(FavoriteQueries).filter_by(user_id=user_id).first()

    def update(self, user_id, **kwargs):
        favorite_query = self.get(user_id)
        for key, value in kwargs.items():
            setattr(favorite_query, key, value)
        return favorite_query

    def delete(self, user_id):
        favorite_query = self.get(user_id)
        self.session.delete(favorite_query)
        return favorite_query

    def commit(self):
        self.session.commit()


pickup_repository = PickUpsRepository(session)
user_repository = TelegramUserRepository(session)
user_queries_repository = UserQueriesRepository(session)
favorite_queries_repository = FavoriteQueriesRepository(session)
