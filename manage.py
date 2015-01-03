import os
from flask.ext.script import Manager
from blog import app
from blog.models import Post
from blog.database import session

manager = Manager(app)

@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod."""

    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

from getpass import getpass

from werkzeug.security import generate_password_hash

from blog.models import User

@manager.command
def adduser():
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()

if __name__ == "__main__":
    manager.run()