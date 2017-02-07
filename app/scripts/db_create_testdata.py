#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Simple script to add multiple selections for testing purposes
'''
import sys
import os
sys.path.append(os.path.abspath('.'))

from app import db
from app.models.user import User
from app.models.course import Course
from app.models.selection import Selection
import random
import re


'''
    Simple algorithm to check if courses overlapped

    Case 1: no overlap (by >= ex)

        bx-----ex
                  by-----ey

    Case 2: no overlap (bx >= ey)

        by-----ey
                  bx-----ex
'''

# check if date time overlapped


def dt_overlap(x, y):
    overlap = True
    dx, tx = x.split("(")
    bx, ex = re.sub(r'[\(\)]', '', tx).split("-")
    dy, ty = y.split("(")
    by, ey = re.sub(r'[\(\)]', '', ty).split("-")

    if dx == dy:
        if by >= ex:
            overlap = False
        elif bx >= ey:
            overlap = False
    else:
        overlap = False

    return overlap


def main():
    for i in xrange(50):
        total = User.query.count()

        courses = [x[0] for x in Course.query.with_entities(Course.cid).all()]

        uid = random.randint(1, total)
        user = User.query.get(uid)

        for j in xrange(3):
            cid = random.choice(courses)
            course = Course.query.get(cid)

            '''
                Check if '1' in student_grade('123456') or 'D' in student_tag('D')
            '''
            if str(user.student_grade) not in course.grades:
                if str(user.student_tag) not in course.grades:
                    continue

            '''
                Check if date time conflicted
            '''
            conflict = False
            selections = Selection.query.filter(Selection.user_id == uid).all()
            for x in selections:
                for dtx in x.course.datetime.split(","):
                    for dty in course.datetime.split(","):
                        if dt_overlap(dtx, dty):
                            conflict = True
                            break
            if conflict:
                continue
            else:
                print(u"{}\t=>\t{}".format(user, course))
                '''
                    Write through to database
                '''
                selection = Selection(user_id=user.uid, course_id=course.cid)
                db.session.add(selection)
                db.session.commit()

if __name__ == '__main__':
    main()
