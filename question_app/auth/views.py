
from flask import render_template, request, redirect, url_for, flash, current_app
from . import auth
from ..models import Question, Comment, Answer, Tag, User
from flask_login import login_user, logout_user, current_user, login_required
from forms import RegisterForm
from ..email import send_email

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        remember_me = request.form.get("remember")
        user = User.objects(name=name).first()
        print current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']
        print current_app.config['MAIL_USERNAME']
        print current_app.config['MAIL_SERVER']
        print current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']

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

@auth.route('/register', methods=["POST","GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.username.data)
        user.password=form.password.data
        user.save()
        print user.email
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                    'confirm',
                    user=user,
                    token=token)
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for("auth.login"))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        current_user.confirmed = True
        flash('You confirmed your account.Thanks!')
    else:
        flash('The confirmation link is Invalid or has expried.')
    return redirect(url_for('main.index'))
