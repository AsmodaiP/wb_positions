from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.scheme import Base

engine = create_engine('sqlite:///test.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
