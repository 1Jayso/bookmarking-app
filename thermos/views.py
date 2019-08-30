from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, current_user, logout_user
# from .forms import BookmarkForm, LoginForm, SignupForm
from . import thermos
from . import forms
from .. import  db, login_manager
from .. import models



@thermos.route('/add', methods= ['GET', 'POST'])
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
        # db.session.add(bm)
        db.session.commit()
        # store_bookmarks(url, description)
        flash("Stored '{}'".format(bm.description))
        return redirect(url_for('main.index'))
    return render_template('bookmark_form.html', form=form, title="Add Bookmark")


@thermos.route('/edit/<int:bookmark_id>', methods=["GET", "POST"])
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
        return redirect(url_for('.user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title="Edit bookmark")


@thermos.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = models.Bookmark.query.get_or_404(bookmark_id)
    if current_user !=  bookmark.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(bookmark)
        db.session.commit()
        flash(f" Deleted '{bookmark.description}'")
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash("Please confirm deleting the bookmark.")
    return render_template('confirm_delete.html', bookmark=bookmark, nolinks =True)

         
@thermos.route('/user/<username>')
@login_required
def user(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
    
@thermos.route('/tag/<name>')
def tag(name):
    tag = models.Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)

