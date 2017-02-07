# -*- coding: utf-8 -*-

import csv
from app import db
from app.models.course import Course

'''
    Import from course file in CSV format into database
'''


def import_course(filename='', replace=False):

    result = False

    with open(filename) as csvfile:
        courses = csv.DictReader(csvfile)
        for row in courses:
            cid = row['課程編號'].decode("UTF-8")
            name = row['課程名稱'].decode("UTF-8")
            description = row['課程敘述'].decode("UTF-8")
            classroom = row['教室'].decode("UTF-8")
            price = row['收費價格'].decode("UTF-8")
            teacher = row['教師'].decode("UTF-8")
            teacher_tag = row['教師說明'].decode("UTF-8")
            teacher_phone = row['教師聯絡電話'].decode("UTF-8")
            grades = row['開課年級'].decode("UTF-8")
            lowbound = row['下限人數'].decode("UTF-8")
            upbound = row['上限人數'].decode("UTF-8")
            datetime = row['上課日期時間'].decode("UTF-8")

            # lookup first
            # unique => grade, class, number
            c = Course.query.filter_by(cid=cid).first()

            # not exist then add a course
            if c is None:
                c = Course(
                    cid=cid,
                    name=name,
                    description=description,
                    classroom=classroom,
                    price=price,
                    teacher=teacher,
                    teacher_tag=teacher_tag,
                    teacher_phone=teacher_phone,
                    grades=grades,
                    lowbound=lowbound,
                    upbound=upbound,
                    datetime=datetime,
                )
                db.session.add(c)
            else:
                # exist then update a ticket
                if replace:
                    c.name = name
                    c.description = description
                    c.classroom = classroom
                    c.price = price
                    c.teacher = teacher
                    c.teacher_tag = teacher_tag
                    c.teacher_phone = teacher_phone
                    c.grades = grades
                    c.lowbound = lowbound
                    c.upbound = upbound
                    c.datetime = datetime
                    c.count = 0

        db.session.commit()
        result = True

    return result
