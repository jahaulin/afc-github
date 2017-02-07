# -*- coding: utf-8 -*-

from app import db
#from app.models.user import User
#from app.models.course import Course
#from app.models.selection import Selection
from app.models.history import History


def logging(user_id=None, message=None, ip=None):
    # add a log entry to table
    history = History(user_id=user_id, message=message, ip=ip)
    db.session.add(history)
    db.session.commit()
