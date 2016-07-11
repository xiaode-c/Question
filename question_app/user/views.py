# coding:utf-8 

from . import user
import os
from flask import current_app
from werkzeug import secure_filename
from flask import render_template, redirect, url_for, request, send_from_directory
from flask_login import login_required
from ..models import User, Question, Tag
import shortuuid

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config["ALLOWED_EXTENSIONS"]

@user.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('user.uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@user.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)


@user.route("/")
@login_required
def index():
    return "hello world"

@user.route("/<name>")
@login_required
def user_info(name):
    usr = User.objects(name=name).first()
    questions = Question.objects(author=usr)
    tags = Tag.objects(author__in=[usr])
    return render_template("user/user.html", user=usr, questions=questions, tags=tags)

@user.route('/<name>/settings', methods=["POST", "GET"])
@login_required
def user_settings(name):
    usr = User.objects(name=name).first()
    if request.method == "POST":
        email = request.form.get("email")
        about_me = request.form.get("about_me")
        usr.email = email
        usr.about_me = about_me
        usr.save()
        return redirect(url_for("user.user_info", name=usr.name))
    return render_template("user/user_settings.html", user=usr)

@user.route('/<name>/change_avatar', methods=["POST", "GET"])
@login_required
def change_avatar(name):
    usr = User.objects(name=name).first()
    if request.method == "POST":
        f = request.files['avatar']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filename = shortuuid.uuid(name=filename)
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            usr.avatar = filename
            usr.save()
            return redirect(url_for('user.user_info',
                                    name=name))
    return render_template("user/change_avatar.html", user=usr) 

# @user.route("/ask", methods=["POST", "GET"])
# @login_required
# def ask():
#     if request.method == "POST":
#         request.form.get("")
