# -*- coding: utf-8 -*-
from app import db
#from app.models.selection import Selection
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"

    uid = db.Column(db.Integer, primary_key=True)      # 唯一編號
    default_password = db.Column(db.Text, default='')  # 預設密碼
    password = db.Column(db.Text, default='')          # 使用者自訂密碼

    ''' student '''
    student_grade = db.Column(db.Integer, default=0)   # 1 ~ 9 年級
    student_class = db.Column(db.Integer, default=0)   # 1 ~ 20 班
    student_number = db.Column(db.Integer, default=0)  # 1 ~ 30 號
    student_name = db.Column(db.Text, default='')      # 學生姓名，中文
    # 特別身份標記，N 無標記、D 舞蹈班、K 幼兒園
    student_tag = db.Column(db.Text, default='N')

    ''' parent '''
    parent_name = db.Column(db.Text, default='')       # 家長姓名，中文
    parent_phone = db.Column(db.Text, default='')      # 0900-123456

    ''' selections '''
    selections = db.relationship("Selection", backref="user", lazy="dynamic")

    ''' multiple fields '''
    __table_args__ = (db.UniqueConstraint(
        'student_grade', 'student_class', 'student_number', name='unique_index_student'), )

    def __init__(self, default_password='', student_grade=0, student_class=0, student_number=0, student_name='', student_tag='N'):
        self.student_grade = student_grade
        self.student_class = student_class
        self.student_number = student_number
        self.student_name = student_name
        self.student_tag = student_tag
        self.default_password = default_password

    def to_json(self):
        return {'uid': self.uid,
                'student_grade': self.student_grade,
                'student_class': self.student_class,
                'student_number': self.student_number,
                'student_name': self.student_name,
                'student_tag': self.student_tag,
                'parent_name': self.parent_name,
                'parent_phone': self.parent_phone,
                'default_password': self.default_password,
                'password': self.password,
                }

    def __repr__(self):
        return "<User '(%d, %d, %d) %s [%s]'>" % (self.student_grade, self.student_class, self.student_number, self.student_name, self.student_tag)

    ''' flask_login.UserMixin '''

    def get_id(self):
        return unicode(self.uid)
