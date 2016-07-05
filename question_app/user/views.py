from . import user
from flask import render_template
from flask_login import login_required
from ..models import User, Question, Tag

@user.route("/")
def index():
    return "hello world"

@user.route("/<name>")
@login_required
def user(name):
    user = User.objects(name=name).first()
    questions = Question.objects(author=user)
    tags = Tag.objects(author__in=[user])
    return render_template("user/user.html", user=user, questions=questions, tags=tags)
