from . import user

@user.route("/")
def index():
    return "hello world"
