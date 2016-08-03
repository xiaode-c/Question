
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user
from datetime import datetime
from . import main
from ..models import Question, Comment, Answer, Tag, User
from flask_login import login_required


def split_tag(tag_str):
    tag_list = tag_str.split(',')
    for i in range(0,len(tag_list)):
        tag_list[i] = tag_list[i].strip()
    tags = []
    for tag in tag_list:
        tag_obj = Tag.objects(name=tag).first()
        if tag_obj is None:
            tag_obj = Tag(name=tag, author=current_user)
            tag_obj.save()
        tags.append(tag_obj)
    return tags


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

@main.route("/ask", methods=["POST", "GET"])
@login_required
def ask():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        tags = split_tag(request.form.get("tags"))
        

        u = User.objects(name=current_user.name).first()
        question = Question(title=title,
                            content=content,
                             created_time=datetime.now(),
                             author=u
                             )
        
        question.tags = tags
        question.save()
        return redirect(url_for("main.index"))
    return render_template("ask.html")

@main.route('/questions/<id>/new_comment', methods=["POST", "GET"])
def new_comment(id):
    if request.method == "POST":
        question = Question.objects(id=id).first()
        content = request.form.get("content")
        parent_id = request.form.get("parent_id")
        author = User.objects(name=current_user.name).first()
        if parent_id == '':
            parent_answer = None
        else:
            parent_answer = Answer.objects(id=parent_id).first()
        dir(current_user)
        ans = Answer(content=content, created_time=datetime.utcnow(), author=author, question=question, parent_answer=parent_answer)
        ans.save()
        return redirect(url_for("main.question_detail", id=id))
    return render_template("main.question_detail", id=id)

@main.route("/follow", methods=["POST", "GET"])
@login_required
def follow():
    question_id = None
    follows = 0
    if request.method == "GET":
        question_id = request.args.get('question_id')
        user = User.objects(id=current_user.id).first()
        Question.objects(id=question_id).update_one(push__follow=user)
        follows = len(Question.objects(id=question_id).first().follow) 
    return jsonify(follows=follows)


