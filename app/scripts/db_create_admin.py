#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Simple script to add administrator
'''
import sys
import os
sys.path.append(os.path.abspath('.'))

from app import db
from app.models.user import User

user = User()

user.uid = 0                        # 'uid = 0' is administrator
user.student_grade = 6
user.student_class = 6
user.student_number = 99
user.student_name = "admin"         # name
user.default_password = "PaSSwoRD"  # password

db.session.add(user)
db.session.commit()
