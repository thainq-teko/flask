from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://teko:1234@localhost:3306/flask_db')


def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def loadBase():
    return Base
