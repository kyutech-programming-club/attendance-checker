from main.models import db, User, Date, init
import datetime
from random import randint, sample 

def make_user():
    for i in range(1, 11):
        user = User(name=str(i))
        db.session.add(user)
    
    db.session.commit()

def make_date():
    d = datetime.datetime(2019, 1, 1)
    while d <= datetime.datetime(2019, 12, 31):
        day = Date(day=d)
        db.session.add(day)
        d += datetime.timedelta(days=1)
    
    db.session.commit()

def make_ralation():
    users = User.query.all()
    for day in Date.query.all():
        user = sample(users, randint(1, 10))
        for u in user:
            day.subscribers.append(u)
        
        db.session.commit()

if __name__ == '__main__':
#    init()
#    make_user()
#    make_date()
#    make_ralation()
