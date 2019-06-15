import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_moment import Moment
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
# from forms import BookmarkForm, LoginForm
import forms


# Flask instance
app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

# app.logger.setLevel(DEBUG)


# Database Configuration
app.config ['SECRET_KEY'] = '\xe6\xb5V\x95>\x9e_z\xa2k\xedH\x81\xc6\xe7\x96\x9f6\xc7\xf0\xa8\x05o{'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)
# bookmarks = []
# def store_bookmarks(url, description):
#     bookmarks.append(dict(
#     url = url,
#     description = description,
#     user = "Joseph",
#     date = datetime.utcnow()
# ))
import models

# def new_bookmarks(num):
#     return sorted(bookmarks, key=lambda bm: bm['date'], reverse= True)[:num]

# Fake login

#Configuration for authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view ="login"
login_manager.init_app(app)

moment = Moment(app)

@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks = models.Bookmark.newest(5))

@app.route('/add', methods= ['GET', 'POST'])
@login_required
def add():
    form = forms.BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        tags = form.tags.data 
        bm = models.Bookmark(user=current_user, url=url, description=description, tags=tags)
        
        # db.session.add(bm)
        current_db_sessions = db.session.object_session(bm)
        current_db_sessions.add(bm)
        db.session.commit()
        # store_bookmarks(url, description)
        flash("Stored '{}'".format(bm.description))
        return redirect(url_for('index'))
    return render_template('bookmark_form.html', form=form, title="Add Bookmark")


@app.route('/edit/<int:bookmark_id>', methods=["GET", "POST"])
@login_required
def edit(bookmark_id):
    bookmark = models.Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = forms.BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)

            # current_user.url = form.url.data
            # current_user.description = form.description.data
            # db.session.add(current_user._get_current_object())
        db.session.commit()
        flash(f"Updated bookmark is {bookmark.description}")
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title="Edit bookmark")


@app.route('/user/<username>')
@login_required
def user(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    
    return render_template('user.html', user=user)
    

@app.route('/login', methods=["GET", "POST"])
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



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=["GET", "POST"])
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

    # if request.method == 'POST':
    #     url = request.form['url']
    #     store_bookmarks(url)
    #     # app.logger.debug('Stored url: ' + url)
    #     flash("Stored bookmark: '{}'".format(url))
    #     # print(bookmarks)
    #     return redirect (url_for('index'))
    # return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)




