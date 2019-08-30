from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, current_user, logout_user
# from .forms import BookmarkForm, LoginForm, SignupForm
from . import auth
from . import forms
from .. import  db, login_manager
from .. import models


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        #login  and validate the user
        user = models.User.get_by_username((form.username.data))

        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfylly as {}".format(user.username))
            return redirect(request.args.get("next") or url_for('user', username=user.username))
        flash("Incorrect username or password")
    return render_template("login.html", form=form)



@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = forms.SignupForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data,
                           username=form.username.data,
                           password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {user.username}! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)










