

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "this too long too strong"
    MAIL_SERVER = u'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USERNAME = u"18710890823@qq.com" #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = u"gaodebao712"  #  os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <18710890823@163.com>'

config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,

}
