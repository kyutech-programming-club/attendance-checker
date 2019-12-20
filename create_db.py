from main.models import db, User, Date, init
import datetime
from random import randint

init()

for i in range(1, 11):
    user = User(name=str(i))
    db.session.add(user)
    db.session.commit()

for user in User.query.all():
    for month in range(1, 12):
        for day in range(1, 29):
            st = randint(11, 18)
            ed = randint(19, 21)

            if st <= 10:
                continue

            st_time = datetime.datetime(2019, month, day, st)
            ed_time = datetime.datetime(2019, month, day, ed)

            date = Date(user_id=user.id, start=st_time, end=ed_time)
            db.session.add(date)
            db.session.commit()

for user in User.query.all():
    print(user.name, "Data")
    for date in user.dates:
        print(" |", date.start, "-", date.end)


