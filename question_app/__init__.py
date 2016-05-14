# coding:utf-8

from flask import Flask
from flask.ext.login import LoginManager
from config import config

login_manager = LoginManager()


def create_app(config_name="default"):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
 
    login_manager.init_app(app)
    #from question_app.model import db\
    from main import main as main_blueprint
    from admin import admin as admin_blueprint
    from user import user as user_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)

    return app
