from flask.ext.script import Manager, Shell
from question_app import create_app
from question_app.models import User, Question, Comment, Tag, Answer


app = create_app()

manager = Manager(app)

#@manager.command
#def initdb:
#    pass

def make_shell_context():
    return dict(app=app, User=User, Question=Question, Comment=Comment, Tag=Tag, Answer=Answer)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__=="__main__":
    manager.run()
