from main import db

user_date_table = db.Table('user_date_tables',
                            db.Column('user_id', 
                                      db.Integer,
                                      db.ForeignKey('users.user_id'),
                                      primary_key=True
                                      ),
                            db.Column('date_id',
                                      db.Integer,
                                      db.ForeignKey('dates.date_id'),
                                      primary_key=True
                                      )
                            )
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, default = 'proken-taro', nullable = False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    dates = db.relationship('Date',
                            secondary=user_date_table, 
                            lazy='subquery', 
                            backref=db.backref('subscribers', lazy='dynamic')
                            )
    times = db.relationship("Time",
                            lazy="select",
                            backref=db.backref("user", lazy='joined')
                            )

    @classmethod
    def authenticate(cls, query, name):
        user = query(cls).filter(cls.name==name).first()
        return user

    def __repr__(self):
        return '<User id={self.user_id} name={self.name!r} active={self.active}>'.format(self=self)

class Date(db.Model):
    __tablename__ = "dates"

    date_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime, nullable=True)
    users = db.relationship('User', 
                            secondary=user_date_table,
                            lazy='subquery',
                            backref=db.backref('subscribers', lazy='dynamic')
                            )
    times = db.relationship("Time",
                            lazy="select",
                            backref=db.backref("date", lazy='joined')
                            )
    members = db.Column(db.Integer, default=0, nullable=True)

    def __repr__(self):
        return '<Id={self.date_id} day={self.day} members={self.members}>'.format(self=self)

class Time(db.Model):
    __tablename__ = "times"

    time_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date_id = db.Column(db.Integer, db.ForeignKey('dates.date_id'))
    start = db.Column(db.DateTime, nullable=True)
    end = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return '<Id={self.time_id} u_id={self.user_id} d_id={self.date_id} start={self.start} end={self.end}>'.format(self=self)

class Proken(db.Model):
    __tablename__ = "prokens"

    proken_id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.Integer)
    members = db.Column(db.Integer)

    def __repr__(self):
        return '<Id={self.proken_id} d_id={self.date_id} members={self.members}>'.format(self=self)

def init():
    db.create_all()
