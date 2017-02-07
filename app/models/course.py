# -*- coding: utf-8 -*-

from app import db
#from app.models.selection import Selection


class Course(db.Model):
    __tablename__ = "course"

    cid = db.Column(db.Integer, primary_key=True)         # 課程編號 105001
    name = db.Column(db.Text, default='')                 # 課程名稱

    ''' place '''
    description = db.Column(db.Text, default='')          # 課程敘述
    classroom = db.Column(db.Text, default='')            # 教室
    price = db.Column(db.Integer, default=0)              # 收費價格 1,500

    ''' teacher '''
    teacher = db.Column(db.Text, default='')              # 教師
    teacher_tag = db.Column(db.Text, default='')          # 教師說明
    teacher_phone = db.Column(db.Text, default='')        # 教師聯絡電話

    ''' limit '''
    grades = db.Column(db.String(10), default='123456')   # 開課年級 123456 KD
    upbound = db.Column(db.Integer, default=15)           # 上限人數，預設 15 人
    lowbound = db.Column(db.Integer, default=9)           # 下限人數，預設 9 人
    # 上課日期時間 1(0800-0900),2(0900-1000)
    datetime = db.Column(db.Text, default='')
    state = db.Column(db.Integer, default=0)              # 課程狀態 0, 1, 2

    ''' aggregate '''
    count = db.Column(db.Integer, default=0)              # 選課人數，揮發性

    ''' selections '''
    selections = db.relationship(
        "Selection", backref="course",  lazy="dynamic")

    def __init__(self,
                 cid='',
                 name='',
                 description='',
                 classroom='',
                 price=0,
                 teacher='',
                 teacher_tag='',
                 teacher_phone='',
                 grades='123456',
                 upbound=15,
                 lowbound=9,
                 datetime='',
                 state=0,
                 count=0,
                 ):
        self.cid = cid
        self.name = name
        ''' place '''
        self.description = description
        self.classroom = classroom
        self.price = price
        ''' teacher '''
        self.teacher = teacher
        self.teacher_tag = teacher_tag
        self.teacher_phone = teacher_phone
        ''' limit '''
        self.grades = grades
        self.upbound = upbound
        self.lowbound = lowbound
        self.datetime = datetime
        self.state = state
        ''' aggragate '''
        self.count = count

    def to_json(self):
        return {'cid': self.cid,
                'name': self.name,
                'description': self.description,
                'classroom': self.classroom,
                'price': self.price,
                'teacher': self.teacher,
                'teacher_tag': self.teacher_tag,
                'teacher_phone': self.teacher_phone,
                'grades': self.grades,
                'upbound': self.upbound,
                'lowbound': self.lowbound,
                'datetime': self.datetime,
                'state': self.state,
                'count': self.count,
                }

    def __repr__(self):
        return "<Course '%d'>" % self.cid
