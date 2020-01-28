from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
import datetime


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    sound_level = Column(Integer, default=0)
    expected_day = Column(DateTime, default=datetime.datetime(2019, 4, 1))

    def __init__(self, user_id=None, sound_level=None, expected_day=None):
        self.user_id = user_id
        self.sound_level = sound_level
        self.expected_day = expected_day

    def __repr__(self):
        return '<id:{self.user_id} sound_level:{self.sound_level} expected_day:{self.expected_day}>'.format(self=self)
