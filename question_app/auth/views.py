
from flask import render_template, request, redirect, url_for, flash
from . import auth
from ..models import Question, Comment, Answer, Tag, User
from flask_login import login_user, logout_user


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        remember_me = request.form.get("remember")
        user = User.objects(name=name).first()
        if user is not None:
            login_user(user, remember_me)
            return redirect(request.args.get('next') or url_for("main.index"))
        flash('Invalid username or password')
    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
