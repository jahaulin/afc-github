# -*- coding: utf-8 -*-

from app import db
import datetime


class Selection(db.Model):
    __tablename__ = "selection"

    sid = db.Column(db.Integer, primary_key=True)           # 選課唯一編號
    user_id = db.Column(db.Integer, db.ForeignKey(          # 使用者 uid
        'user.uid'), nullable=False)
    #
    course_id = db.Column(db.Integer, db.ForeignKey(        # 課程 cid
        'course.cid'), nullable=False)
    #
    priority = db.Column(db.Integer, default=0)             # 優先權
    #
    timestamp = db.Column(db.DateTime(timezone=True),       # 選擇時間紀錄
                          default=datetime.datetime.utcnow)

    def __init__(self, user_id=0, course_id=0, priority=0):
        self.user_id = user_id
        self.course_id = course_id
        self.priority = priority

    def to_json(self):
        return {'sid': self.sid,
                'user_id': self.user_id,
                'course_id': self.course_id,
                'priority': self.priority,
                'timestamp': self.timestamp,
                }

    def __repr__(self):
        return "<Selection '%r'>" % self.sid
