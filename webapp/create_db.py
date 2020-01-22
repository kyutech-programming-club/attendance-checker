from main.models import db, User, Date, Time, init
import datetime
from random import randint, sample 

def make_user():
    for i in range(1, 11):
        user = User(name=str(i))
        db.session.add(user)
    
    db.session.commit()

def make_date():
    d = datetime.datetime(2019, 1, 1)
    while d <= datetime.datetime(2020, 12, 31):
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

def make_time():
    users = User.query.all()
    dates = Date.query.all()
    
    for user in users:
        for date in user.dates:

            s = datetime.time(randint(15, 18), 0, 0)
            e = datetime.time(randint(19, 22), 0, 0)
            start = datetime.datetime.combine(date.day, s)
            end = datetime.datetime.combine(date.day, e)
            t = Time(user=user, date=date, start=start, end=end)
            db.session.add(t)

    db.session.commit()

def make_proken():
    for date in Date.query.all():
        members = 0
        for user in date.users:
            if user is None:
                continue
            members += 1
            
        date.members = members
        db.session.add(date)

    db.session.commit()

if __name__ == '__main__':
    init()
    make_user()
    make_date()
    make_ralation()
    make_time()
    make_proken()

    '''
    for date in Date.query.all():
        print(date.day, "の活動")
        for user in date.users:
            time = Time.query.filter_by(user_id=user.user_id).filter_by(date_id=date.date_id).first()
            print(user.name, ":", time.start.hour, "~", time.end.hour)

    '''
    for date in Date.query.all():
        print(date.day, ":", date.members)


