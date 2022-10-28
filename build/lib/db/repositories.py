from scheme import TelegramUser, UserQueries, Positions, Base, PickUps
from db import session


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


class PickUpsRepository(BaseRepository):
    def __init__(self, session):
        self.session = session

    def create(self, address, latitude, longitude):
        pickup = PickUps(
            address=address,
            latitude=latitude,
            longitude=longitude,
        )
        self.session.add(pickup)
        return pickup

    def get(self, pickup_id):
        return self.session.query(PickUps).filter_by(id=pickup_id).first()
    
    def get_by_address(self, address):
        return self.session.query(PickUps).filter_by(address=address).first()

    def update(self, pickup_id, **kwargs):
        pickup = self.get(pickup_id)
        for key, value in kwargs.items():
            setattr(pickup, key, value)
        return pickup

    def delete(self, pickup_id):
        pickup = self.get(pickup_id)
        self.session.delete(pickup)
        return pickup

    def commit(self):
        self.session.commit()

    def get_all(self):
        return self.session.query(PickUps).all()

    def get_all_by_user(self, user_id):
        return self.session.query(PickUps).filter_by(user_id=user_id).all()

    def get_all_by_user_and_status(self, user_id, status):
        return self.session.query(PickUps).filter_by(user_id=user_id, status=status).all()

    def get_all_by_status(self, status):
        return self.session.query(PickUps).filter_by(status=status).all()

    def get_all_by_status_and_time(self, status, time):
        return self.session.query(PickUps).filter_by(status=status, time=time).all()

    def get_all_by_status_and_time_and_user(self, status, time, user_id):
        return self.session.query(PickUps).filter_by(status=status, time=time, user_id=user_id).all()

    def get_all_by_status_and_time_and_user_and_type(self, status, time, user_id, type):
        return self.session.query(PickUps).filter_by(status=status, time=time, user_id=user_id, type=type).all()

    def get_all_by_status_and_time_and_type(self, status, time, type):
        return self.session.query(PickUps).filter_by(status=status, time=time, type=type).all()

    def get_all_by_status_and_time_and_user_and_type_and_address(self, status, time, user_id, type, address):
        return self.session.query(PickUps).filter_by(status=status, time=time, user_id=user_id, type=type, address=address).all()


class TelegramUserRepository(BaseRepository):
    def create(self, chat_id, username, first_name, last_name):
        user = TelegramUser(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
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
    



