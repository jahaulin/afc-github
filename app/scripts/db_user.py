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

manager = Manager(app)


@manager.command
@manager.option('-f', '--filename', help='Filename')
@manager.option('-t', '--tag', help='Student tag')
def update_tag(filename=None, tag="N"):

    with open(filename, "r") as f:
        for line in f.readlines():
            classname, student_name = re.split(r'\s+', line.strip(), maxsplit=2)
            student_name = student_name.decode("UTF-8")

            student_grade = int(classname[0:1])
            student_class = int(classname[1:])
            user = User.query.filter(User.student_name == student_name).filter(
                User.student_grade == student_grade).filter(User.student_class == student_class).first()

            if user:
                user.student_tag = tag
                db.session.add(user)

                print(json.dumps(user.to_json(), ensure_ascii=False,
                                 sort_keys=True).encode('UTF-8'))

    db.session.commit()

@manager.command
@manager.option('-u', '--uid', help='User id')
def export(uid=0):
    #    print("Filename: {}".format(filename))

    user = User.query.get(uid)

    if user:
        print(json.dumps(user.to_json(), ensure_ascii=False,
                         sort_keys=True).encode('UTF-8'))


@manager.command
@manager.option('-n', '--name', help='Field name')
@manager.option('-v', '--value', help='Field value')
def edit(name='', value=''):
    data = "".join(sys.stdin.readlines())
    user = json.loads(data)
    user[name] = value
    print(json.dumps(user, ensure_ascii=False, sort_keys=True).encode('UTF-8'))


@manager.command
def update():
    data = "".join(sys.stdin.readlines())
    j = json.loads(data)
    user = User.query.get(j['uid'])

    for attr in j.keys():
        if attr != 'uid':
            setattr(user, attr, j[attr])

    db.session.add(user)
    db.session.commit()

    print(json.dumps(user.to_json(), ensure_ascii=False,
                     sort_keys=True).encode('UTF-8'))

if __name__ == '__main__':
    manager.run()
