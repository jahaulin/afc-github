#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath('.'))

import csv
from flask_script import Manager
from app import db, app
from app.models.user import User

manager = Manager(app)


@manager.command
@manager.option('-f', '--filename', help='filename of CSV')
@manager.option('-r', '--replace', help='Update, replace all records')
def import_user(filename='', replace=False):
    print("Filename: {}".format(filename))
    print(" Replace: {}".format(replace))

    with open(filename) as csvfile:
        students = csv.DictReader(csvfile)
        for row in students:
            student_grade = row['年級']
            student_class = row['班級']
            student_number = row['座號']
            student_name = row['學生姓名'].decode("UTF-8")  # unicode
            student_tag = row['註記'].decode("UTF-8")       # N, D, K, H
            default_password = ('' + row['身分證字號'])[-4:]

            # lookup first
            # unique => grade, class, number
            t = User.query.filter_by(
                student_grade=student_grade,
                student_class=student_class,
                student_number=student_number).first()

            # not exist then add a ticket
            if t is None:
                t = User(
                    student_grade=student_grade,
                    student_class=student_class,
                    student_number=student_number,
                    student_name=student_name,
                    student_tag=student_tag,
                    default_password=default_password,
                )
                db.session.add(t)
            else:
                # exist then update a ticket
                if replace:
                    t.student_name = student_name
                    t.student_tag = student_tag
                    t.default_password = default_password

        db.session.commit()

if __name__ == '__main__':
    manager.run()
