import os
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from logging import DEBUG
from forms import BookmarkForm, LoginForm, SignupForm

import models

from thermos import app, db, login_manager

basedir = os.path.abspath(os.path.dirname(__file__))

app.logger.setLevel(DEBUG)


class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return "{}. {}.".format(self.firstname[0], self.lastname[0])


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Greatest title ever",
                           user=User("Juan", "Ponce"),
                           new_bookmarks=models.Bookmark.newest(10))


@app.errorhandler(404)
def page_not_found(d):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return "Server Error : 500 : '{}'".format(e), 500


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    app.logger.debug("flag")
    form = BookmarkForm()
    if request.method == "POST" and form.Ourvalidate():
        app.logger.debug("flag")
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        app.logger.debug('stored url: ' + url)
        flash("Success : Stored Bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/user/<username>')
def user(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(int(userid))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data,
                           username=form.username.data,
                           password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Login and validate the user ...
        user = models.User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user',
                                                                username=user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))