from main import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, default = 'proken-taro', nullable = False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    dates = db.relationship("Date", lazy="select", backref=db.backref("user", lazy='joined'))
    @classmethod
    def authenticate(cls, query, name):
        user = query(cls).filter(cls.name==name).first()
        return user

    def __repr__(self):
        return '<User id={self.id} name={self.name!r} active={self.active}>'.format(self=self)

class Date(db.Model):
    __tablename__ = "dates"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start = db.Column(db.DateTime, nullable=True)
    end = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Id={self.id} User id={self.user_id} start={self.start} end={self.end}>'.format(self=self)

class Proken(db.Model):
    __tablename__ = "prokens"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime)
    prokens = db.Column(db.Integer)

    def __repr__(self):
        return '<Id={self.id} Day={self.day} Prokens={self.prokens}>'.format(self=self)

def init():
    db.create_all()
