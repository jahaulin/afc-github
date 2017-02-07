# -*- coding: utf-8 -*-
from app import db
import datetime


class History(db.Model):
    __tablename__ = "history"

    hid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.uid"), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.utcnow)
    message = db.Column(db.String(1024))
    ip = db.Column(db.String(40))

    user = db.relationship("User", foreign_keys="History.user_id")

    def __init__(self, user_id=0, message='', ip=''):
        self.user_id = user_id
        self.message = message
        self.ip = ip

    def __repr__(self):
        return "<History '%d'>" % self.hid
