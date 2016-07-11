# coding:utf-8
import os

a = os.path.dirname(os.path.abspath("__file__"))


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "this too long too strong"
    UPLOAD_FOLDER = os.path.join(a, "question_app/static/uploads")
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "email_username"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "email_password"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    FLASKY_MAIL_SUBJECT_PREFIX = '<NOTE>'
    FLASKY_MAIL_SENDER = 'NOTE Admin <%s>' % os.environ.get('MAIL_USERNAME')
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024

config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,

}
