
from flask import render_template, request, redirect, url_for, flash, current_app
from . import auth
from ..models import Question, Comment, Answer, Tag, User
from flask_login import login_user, logout_user, current_user, login_required
from forms import RegisterForm
from ..email import send_email
# import smtplib
# from email import encoders
# from email.header import Header
# from email.mime.text import MIMEText
# from email.utils import parseaddr, formataddr

# from .. import mail
# from threading import Thread
# from flask.ext.mail import Message

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# def send_email(to, subject, template, **kwargs):
#     msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
#     sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[current_app, msg])
#     thr.start()
#     return thr



# def _format_addr(s):
#     name, addr = parseaddr(s)
#     return formataddr(( \
#         Header(name, 'utf-8').encode(), \
#         addr.encode('utf-8') if isinstance(addr, unicode) else addr))


# def send_email(from_addr, to_addr, subject, password, template):
#     msg = MIMEText(render_template(template + '.html'),'html','utf-8')
#     msg['Subject'] = subject
#     msg['From'] = _format_addr(u'<%s>' % from_addr)
#     msg['To'] = _format_addr(u'<%s>' % to_addr)
#     msg['Subject'] = Header(subject, 'utf-8').encode()

#     smtp = smtplib.SMTP()
#     smtp.connect('smtp.163.com')
#     server.set_debuglevel(1)
#     smtp.login(from_addr, password)
#     smtp.sendmail(from_addr, to_addr, msg.as_string())
#     smtp.quit()


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
        token = user.generate_confirmation_token()
        send_email(user.email, 'COnfirm Your Account',
                    'confirm',
                    user=user,
                    token=token)
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for("auth.login"))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmd:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You confirmed your account.Thanks!')
    else:
        flash('The confirmation link is Invalid or has expried.')
    return redirect(url_for('main.index'))
