# -*- coding: utf-8 -*-

import re
from app import app, login_manager, db
from app.models.user import User
from app.models.course import Course
from app.models.selection import Selection
from app.tools.log import logging
from flask_login import login_required
from flask import render_template, url_for, redirect, request, flash, abort, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
from wtforms.fields.html5 import TelField
from flask_babel import gettext as _, lazy_gettext
from datetime import datetime
from functools import wraps

'''
    Date time constraint decorator
'''


def datetime_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        now = app.config.get('DATETIME_TZ').fromutc(datetime.utcnow())
        if now < app.config.get('DATETIME_BEGIN'):
            return error_page(errors=[lazy_gettext('This is not a registration time!'),
                                      lazy_gettext(
                                          'Begin time: ') + app.config.get('DATETIME_BEGIN').strftime("%F %T (%z)"),
                                      lazy_gettext(
                                          'End time: ') + app.config.get('DATETIME_END').strftime("%F %T (%z)"),
                                      ])
        elif now > app.config.get('DATETIME_END'):
            return error_page(errors=[lazy_gettext('This is not a registration time!'),
                                      lazy_gettext(
                                          'Begin time: ') + app.config.get('DATETIME_BEGIN').strftime("%F %T (%z)"),
                                      lazy_gettext(
                                          'End time: ') + app.config.get('DATETIME_END').strftime("%F %T (%z)"),
                                      ])
        else:
            return f(*args, **kwargs)

    return decorated_function


def error_page(error_title=lazy_gettext('Error'), errors=[]):
    return render_template("error.html", error_title=error_title, errors=errors)


'''
    Required field constraint decorator
'''


def field_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (not g.user.parent_phone) or (not g.user.parent_name):
            flash(_("Update parent profile first!"))
            return redirect(url_for('user'))
        else:
            return f(*args, **kwargs)

    return decorated_function


'''
    Edit parent information
'''


class ParentForm(FlaskForm):
    parent_name = StringField(lazy_gettext("Parent name"), render_kw={
                              "placeholder": lazy_gettext("Wang's mother")}, validators=[DataRequired()])
    parent_phone = TelField(lazy_gettext("Parent phone"), render_kw={
                            "placeholder": lazy_gettext("06-2133007 or 0912-345678")}, validators=[DataRequired()])
    submit = SubmitField(lazy_gettext("Update"))


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

'''
    Get user information
'''


@app.route("/user", methods=["GET"])
@login_required
def user():
    form = ParentForm(obj=g.user)
    return render_template("user.html", form=form)

'''
    Edit user information about parent
'''


@app.route("/user/<int:uid>", methods=["POST"])
@login_required
def update_user(uid):

    # must be youself
    if g.user.uid != uid:
        abort(403)

    form = ParentForm(obj=g.user)
    if form.validate_on_submit():

        parent_name = request.form["parent_name"]
        parent_phone = request.form["parent_phone"]

        if g.user:
            g.user.parent_name = parent_name
            g.user.parent_phone = parent_phone
            db.session.add(g.user)
            db.session.commit()
            flash(_("Parent profile updated!"))

    else:
        flash(_("Update parent profile first!"))

    return redirect(url_for("user"))

'''
    Get all courses information
'''


@app.route("/course", methods=["GET"])
@login_required
@field_required
def course():
    courses = Course.query.order_by(Course.cid.asc()).all()
    selections = Selection.query.filter(Selection.user_id == g.user.uid)
    selected = {}
    for s in selections:
        selected[s.course_id] = True

    return render_template("course.html", courses=courses, selected=selected)


@app.route("/course/list", methods=["GET"])
def course_list():
    courses = Course.query.order_by(Course.cid.asc()).all()

    return render_template("course_list.html", courses=courses)

'''
    Simple algorithm to check if courses overlapped

    Case 1: no overlap (by >= ex)

        bx-----ex
                  by-----ey

    Case 2: no overlap (bx >= ey)

        by-----ey
                  bx-----ex
'''


def dt_overlap(x, y):
    overlap = True
    dx, tx = x.split("(")
    bx, ex = re.sub(r'[\(\)]', '', tx).split("-")
    dy, ty = y.split("(")
    by, ey = re.sub(r'[\(\)]', '', ty).split("-")

    if dx == dy:
        if by >= ex:
            overlap = False
        elif bx >= ey:
            overlap = False
    else:
        overlap = False

    return overlap

'''
    Selections (user-course pairs)
'''


@app.route("/selection", methods=["GET"])
@login_required
def selection():
    selections = Selection.query.filter(
        Selection.user_id == g.user.uid).order_by(Selection.course_id).all()

    weeks = {}
    ranks = {}
    counts = {}
    valids = {}

    for i in xrange(1, 8):
        weeks[i] = []

    for s in selections:
        ranks[s.course_id] = Selection.query.filter(Selection.course_id == s.course_id).filter(
            Selection.sid <= s.sid).count()
        counts[s.course_id] = Selection.query.filter(
            Selection.course_id == s.course_id).count()

        if s.course.lowbound <= counts[s.course_id] and ranks[s.course_id] <= s.course.upbound:
            valids[s.course_id] = True
        else:
            valids[s.course_id] = False

        '''
        if counts[s.course_id] >= s.course.lowbound:
            dt = s.course.datetime
            weeks[int(dt[0])].append(dt)
        '''
        # may contain multiple datetimes
        for dt in s.course.datetime.split(","):
            weeks[int(dt[0])].append(dt)

    for i in xrange(1, 8):
        weeks[i].sort()

    return render_template("selection.html", selections=selections, ranks=ranks, weeks=weeks, counts=counts, valids=valids)

'''
    User select a course
'''


@app.route("/selection/<int:uid>/<int:cid>", methods=["GET"])
@login_required
@datetime_required
def create_selection(uid=0, cid=0):
    '''
    1. check user login/authenticated
    2. uid = g.user.uid
    3. valid cid
       a. exist
       b. cid grade, datetime, upbound, state
    4. (uid, cid) not in selection
    '''

    # same user id, self
    if g.user.uid != uid:
        abort(403)

    # valid course id
    course = Course.query.filter(Course.cid == cid).first()
    if course is None:
        abort(403)

    # check course state
    if course.state != 0:
        flash(_('ERROR: Course cannot be selected!'))
        return render_template("create_selection.html", course=course)

    # user's grade OR user's tag in course's grades
    if str(g.user.student_grade) not in course.grades:
        if str(g.user.student_tag) not in course.grades:
            flash(_('ERROR: Grade is not in course!'))
            return render_template("create_selection.html", course=course)

    # already selected
    selection = Selection.query.filter(Selection.user_id == uid).filter(
        Selection.course_id == cid).first()
    if selection:
        flash(_('WARNING: You have selected this course!'))
    else:
        conflict = False
        selections = Selection.query.filter(Selection.user_id == uid).all()
        for x in selections:
            for dtx in x.course.datetime.split(","):
                for dty in course.datetime.split(","):
                    if dt_overlap(dtx, dty):
                        conflict = True
                        break
        if conflict:
            flash(_('ERROR: Date time conflicted!'))
            return render_template("create_selection.html", course=course)

        selection = Selection(user_id=uid, course_id=cid)
        db.session.add(selection)
        db.session.commit()
        flash(_('You selected this course.'))
        logging(user_id=g.user.uid, message="User selected a course. (course_id={})".format(
            cid), ip=request.remote_addr)

    rank = Selection.query.filter(Selection.course_id == cid).filter(
        Selection.sid <= selection.sid).count()

    return render_template("create_selection.html", course=course, rank=rank)

'''
    User deselect a course
'''


@app.route("/deselection/<int:uid>/<int:cid>", methods=["GET"])
@login_required
@datetime_required
def delete_selection(uid=0, cid=0):
    '''
    1. check user login/authenticated
    2. uid = g.user.uid
    '''

    # same user id, self
    if g.user.uid != uid:
        abort(403)

    # already selected
    selection = Selection.query.filter(Selection.user_id == uid).filter(
        Selection.course_id == cid).first()
    if not selection:
        flash(_('ERROR: You did not select this course!'))
    else:
        db.session.delete(selection)
        db.session.commit()
        flash(_('You have deselected this course.'))
        logging(user_id=g.user.uid, message="User deselected a course. (course_id={})".format(
            cid), ip=request.remote_addr)

    return redirect(request.referrer or url_for("selection"))

'''
    Just show contact information
'''


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")
