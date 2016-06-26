
from flask import render_template
from . import main
from ..models import Question, Comment, Answer, Tag


@main.route("/", methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@main.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    pagination = Question.pagination(page, 10)
    questions = pagination.items
    print pagination.items
    # print current_user
    return render_template("index.html", questions=questions,
                           pagination=pagination)


@main.route("/questions/<id>")
def question_detail(id):
    question = Question.objects(id=id).first()
    comments = Comment.objects.filter(content_object=question)
    answers = Answer.objects.filter(question=question)
    return render_template("details.html", question=question,
                           comments=comments, answers=answers)


@main.route("/tags")
def tags():
    tags = Tag.objects
    return render_template("tags.html", tags=tags)


@main.route("/tags/<name>")
def tag(name):
    tag = Tag.objects(name=name).first()
    questions = Question.objects(tags__in=[tag])
    print questions
    return render_template("tag.html", tag=tag)


# @main.route("/ask")
# def ask():
#     if request.method == "POST":
#         name = request.form.get("content")
#         password = request.form.get("tags")

#         user = User.objects(name=name).first()
#         if user is not None:
#             login_user(user, remember_me)
#             return redirect(request.args.get('next') or url_for("main.index"))
#         flash('Invalid username or password')
#     return render_template("answer.html")
