from main import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, default = 'proken-taro', nullable = False)

    def __repr__(self):
        return '<User id={self.id} name={self.name!r}>'.format(self=self)


def init():
    db.create_all()
