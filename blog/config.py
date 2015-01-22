import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog-development.db"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog-testing.db"
    DEBUG = False
    SECRET_KEY = "Not secret"


