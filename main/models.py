from main import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, default = 'proken-taro', nullable = False)

    @classmethod
    def authenticate(cls, query, name):
        user = query(cls).filter(cls.name==name).first()
        return user

    def __repr__(self):
        return '<User id={self.id} name={self.name!r}>'.format(self=self)


def init():
    db.create_all()
