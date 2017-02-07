# -*- coding: utf-8 -*-

import os
from datetime import timedelta, datetime
import pytz
basedir = os.path.abspath(os.path.dirname(__file__))

# deployment config
DEBUG = True
TESTING = True

# security config
SECRET_KEY = "default_SECRET_KEY"
WTF_CSRF_ENABLED = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

# database config
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,  "db_repository")
SQLALCHEMY_TRACK_MODIFICATIONS = True

# language config
BABEL_DEFAULT_LOCALE = "zh"
BABEL_DEFAULT_TIMEZONE = "Asia/Taipei"
LOGIN_MESSAGE = u"請先登入以存取這個頁面。"

# school config
SCHOOL_NAME = u"臺南市進學國小"
SCHOOL_URL = u"//www.chps.tn.edu.tw/"
SCHOOL_IT_URL = u"http://www.chps.tn.edu.tw/dokuwiki/academic#資訊組"
SCHOOL_HELP_URL = u"http://www.chps.tn.edu.tw/dokuwiki/activity:afterschool"

# datetime config
DATETIME_TZ = pytz.timezone('Asia/Taipei')
''' year, month, day, hour, minute, second, microsecond, tzinfo'''
DATETIME_BEGIN = DATETIME_TZ.localize(datetime(2017, 2, 2, 9, 0, 0, 0))
#DATETIME_BEGIN = DATETIME_TZ.localize(datetime(2017, 2, 19, 9, 0, 0, 0))
DATETIME_END = DATETIME_TZ.localize(datetime(2017, 2, 21, 18, 0, 0, 0))
