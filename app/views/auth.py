# -*- coding: utf-8 -*-

from app import app, login_manager
from app.models.user import User
from app.tools.log import logging
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, url_for, redirect, request, abort, flash, g
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField, SelectField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from app.authenticator import StudentAuthenticator
from flask_babel import gettext as _, lazy_gettext

'''
    Forms
'''


class LoginForm(FlaskForm):
    student_grade = SelectField(
        lazy_gettext("Grade"), choices=[('0', lazy_gettext('Kindergarten')), ('1', lazy_gettext('1st grade')), ('2', lazy_gettext('2nd grade')), ('3', lazy_gettext('3rd grade')), ('4', lazy_gettext('4th grade')), ('5', lazy_gettext('5th grade')), ('6', lazy_gettext('6th grade'))])
    student_class = SelectField(
        lazy_gettext("Class"), choices=[('1', lazy_gettext('Penguin')), ('2', lazy_gettext('Rabbit')), ('3', lazy_gettext('Zebra')), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')])
    student_number = TextField(
        lazy_gettext("Number"), validators=[DataRequired()], render_kw={'placeholder': lazy_gettext('1, 2, ...')})
    ''' omit the name field
    student_name = TextField(
        lazy_gettext("Name"), validators=[DataRequired()], render_kw={'placeholder': lazy_gettext('Chinese name')})
    '''
    password = PasswordField(
        lazy_gettext("Password"), validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(lazy_gettext("Login"))
    next = HiddenField("Next")

'''
    Login Manager
'''


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.before_request
def before_request():
    g.user = current_user

'''
    User Login
'''


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user and g.user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    target = request.args.get("next") or request.referrer or None
    form.next.data = target

    if form.validate_on_submit():
        student_grade = request.form["student_grade"]
        student_class = request.form["student_class"]
        student_number = request.form["student_number"]
        ''' omit the name field
        student_name = request.form["student_name"]
        '''
        password = request.form["password"]
        target = request.form["next"]

        # authenticate via Student Profile
        stu_auth = StudentAuthenticator(
            student_grade=student_grade, student_class=student_class, student_number=student_number, password=password)
        if not stu_auth.authenticate():
            abort(401)

        # authenticated
        user = User.query.filter_by(
            student_grade=student_grade,  student_class=student_class,  student_number=student_number).first()
        target = target or url_for("index")

        login_user(user)
        flash(_("You have logged in!"))
        logging(user_id=g.user.uid, message="User logged in.",
                ip=request.remote_addr)

        return redirect(target)

    return render_template("login.html", form=form)


'''
    User Logout
'''


@app.route("/logout")
@login_required
def logout():
    previous_uid = g.user.uid

    logout_user()
    flash(_("You have logged out!"))
    logging(user_id=previous_uid, message="User logged out.",
            ip=request.remote_addr)
    return redirect(url_for("login"))

'''
    Default Index Page
'''


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
