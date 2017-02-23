#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath('.'))

import re
import json
from flask_script import Manager
from app import app, db
from app.models.user import User
from app.models.course import Course
from app.models.selection import Selection

manager = Manager(app)


@manager.command
@manager.option('-g', '--grade', help='Student grade')
@manager.option('-c', '--class_', help='Student class')
@manager.option('-n', '--number', help='Student number')
def get(grade=0, class_=0, number=0):

    user = User.query.filter(User.student_grade == grade).filter(
        User.student_class == class_).filter(User.student_number == number).first()

    if user:
        print(u"Grade:   {}".format(user.student_grade))
        print(u"Class:   {}".format(user.student_class))
        print(u"Number:  {}".format(user.student_number))
        print(u"Name:    {}".format(user.student_name))
        print(u"User id: {}".format(user.uid))
        print("")

        uid = user.uid

        selections = Selection.query.filter(Selection.user_id == uid)

        if selections:
            for s in selections:
                print(u"\t[{}]".format(s.sid))
                print(u"\tCourse id:   {}".format(s.course_id))
                print(u"\tCourse name: {}".format(s.course.name))
                print("")
        else:
            print("ERROR: Selection not found.")
    else:
        print("ERROR: User not found.")


@manager.command
@manager.option('-u', '--uid', help='User id')
@manager.option('-c', '--cid', help='Course id')
@manager.option('-y', '--yes', help='Do it')
def delete(uid=None, cid=None, yes=False):

    if uid is None or cid is None:
        print("ERROR: Both uid and cid cannot be empty.")
        return

    selection = Selection.query.filter(Selection.user_id == uid).filter(
        Selection.course_id == cid).first()

    if selection:
        print(u"Student name: {}".format(selection.user.student_name))
        print(u"Course name:  {}".format(selection.course.name))

        if yes:
            db.session.delete(selection)
            db.session.commit()
    else:
        print("ERROR: Selection not found.")


@manager.command
@manager.option('-u', '--uid', help='User id')
@manager.option('-c', '--cid', help='Course id')
@manager.option('-y', '--yes', help='Do it')
def add(uid=None, cid=None, yes=False):

    if uid is None or cid is None:
        print("ERROR: Both uid and cid cannot be empty.")
        return

    user = User.query.filter(User.uid == uid).first()
    course = Course.query.filter(Course.cid == cid).first()

    if user and course:
        print(u"Student name: {}".format(user.student_name))
        print(u"Course name:  {}".format(course.name))

        if yes:
            selection = Selection(user_id=user.uid, course_id=course.cid)
            db.session.add(selection)
            db.session.commit()
    else:
        print("ERROR: Either user or course are not found.")


if __name__ == '__main__':
    manager.run()
