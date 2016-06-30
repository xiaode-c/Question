import os

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "this too long too strong"
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "email_username"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "email_password"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[NOTE]'
    FLASKY_MAIL_SENDER = 'NOTE Admin '

config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,

}
