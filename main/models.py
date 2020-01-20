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

    def __repr__(self):
        return '<Id={self.date_id} day={self.day}>'.format(self=self)

class Proken(db.Model):
    __tablename__ = "prokens"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime)
    prokens = db.Column(db.Integer)

    def __repr__(self):
        return '<Id={self.id} Day={self.day} Prokens={self.prokens}>'.format(self=self)

def init():
    db.create_all()
