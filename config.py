

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "this too long too strong"

config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,

}
