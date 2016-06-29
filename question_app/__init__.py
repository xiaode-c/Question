# coding:utf-8

from flask import Flask
from flask.ext.login import LoginManager
# from flask.ext.moment import Moment
from flask.ext.mail import Mail
from config import config

login_manager = LoginManager()
mail = Mail()
# moment = Moment()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    login_manager.init_app(app)
    mail.init_app(app)
    # moment.init_app(app)
    #from question_app.model import db\
    from main import main as main_blueprint
    from admin import admin as admin_blueprint
    from user import user as user_blueprint
    from auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)

    # from admin import UserView
    # from models import User
    # admin.add_view(UserView(User))

    return app
