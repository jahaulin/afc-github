#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath('.'))

import csv
from flask_script import Manager
from app import app
from app.models.course import Course

manager = Manager(app)


@manager.command
@manager.option('-f', '--filename', help='filename of CSV')
def export_course(filename=''):
    print("Filename: {}".format(filename))

    courses = Course.query.order_by(Course.cid).all()

    with open(filename, 'w') as csvfile:
        fieldnames = [
            '課程編號',
            '課程名稱',
            '課程敘述',
            '教室',
            '收費價格',
            '教師',
            '教師說明',
            '教師聯絡電話',
            '開課年級',
            '下限人數',
            '上限人數',
            '上課日期時間',
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for c in courses:
            row = {
                '課程編號': c.cid,
                '課程名稱': c.name.encode("UTF-8"),
                '課程敘述': c.description.encode("UTF-8"),
                '教室': c.classroom.encode("UTF-8"),
                '收費價格': c.price,
                '教師': c.teacher.encode("UTF-8"),
                '教師說明': c.teacher_tag.encode("UTF-8"),
                '教師聯絡電話': c.teacher_phone,
                '開課年級': c.grades,
                '下限人數': c.lowbound,
                '上限人數': c.upbound,
                '上課日期時間': c.datetime,
            }
            writer.writerow(row)

if __name__ == '__main__':
    manager.run()
