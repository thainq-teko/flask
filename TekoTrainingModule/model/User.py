import json

from sqlalchemy import Column, Integer, String, create_engine
engine = create_engine('mysql://teko:1234@localhost:3306/flask_db')


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)  # type: object
    username = Column(String)
    password = Column(String)
    email = Column(String)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        user = dict()
        user['username'] = self.username
        user['password'] = self.password
        return json.dumps(user)
