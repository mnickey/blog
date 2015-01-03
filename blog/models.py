import datetime

from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime
from database import Base, engine

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, Sequence("post_id_sequence"), primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)

from flask.ext.login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_sequence"), primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

Base.metadata.create_all(engine)
