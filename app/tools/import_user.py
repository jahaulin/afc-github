# -*- coding: utf-8 -*-

import csv
from app import db
from app.models.user import User


'''
    Import from user file in CSV format into database
'''


def import_user(filename='', replace=False):

    result = False

    with open(filename) as csvfile:
        students = csv.DictReader(csvfile)
        for row in students:
            student_grade = row['年級'].decode("UTF-8")
            student_class = row['班級'].decode("UTF-8")
            student_number = row['座號'].decode("UTF-8")
            student_name = row['學生姓名'].decode("UTF-8")  # unicode
            student_tag = row['註記'].decode("UTF-8")       # N, D, K, H
            # only the last 4 digits
            default_password = (('' + row['身分證字號']).decode("UTF-8"))[-4:]

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
        result = True

    return result
