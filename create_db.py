from main.models import db, User, Date, init, Proken
import datetime
from random import randint

init()

for i in range(1, 11):
    user = User(name=str(i))
    db.session.add(user)
    db.session.commit()

for user in User.query.all():
    user_mind = randint(11, 17)
    for month in range(1, 12):
        for day in range(1, 29):
            st = randint(11, 17)
            ed = randint(17, 21)

            if st < user_mind:
                continue

            st_time = datetime.datetime(2019, month, day, st)
            ed_time = datetime.datetime(2019, month, day, ed)

            date = Date(user_id=user.id, start=st_time, end=ed_time)
            db.session.add(date)
            db.session.commit()

dates = Date.query.order_by(Date.end).all()
days = []
for date in dates:
    days.append(date.end.date())
days_set = set(days)
days_list = list(days_set)
days_list = sorted(days_list)
for day in days_list:
    db_day = day
    db_prokens = days.count(day)
    prokens = Proken(day=db_day, prokens=db_prokens)
    db.session.add(prokens)
    db.session.commit()

for proken in Proken.query.all():
    print(proken)


