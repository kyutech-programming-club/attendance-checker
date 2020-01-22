from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    sound = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.datetime(2019, 4, 1))

    def __init__(self, name=None, sound=None, date=None):
        self.name = name
        self.sound = sound
        self.date = date

    def __repr__(self):
        return '<id:{self.id} name:{self.name} sound:{self.sound} date:{self.date}>'.format(self=self)
