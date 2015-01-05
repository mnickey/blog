from flask import render_template

from blog import app
from database import session
from models import Post
from flask.ext.login import login_required

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc()) # change to desc for descending order
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")

import mistune
from flask import request, redirect, url_for

@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        #was content=mistune.markdown(request.form["content"]) ) but was seeing html tags in posts
        content=request.form["content"],
        author = current_user)
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

@app.route("/post/<int:post_id>", methods=["GET"])
def view_post(post_id):
    posts = session.query(Post)
    posts = posts.filter(Post.id == post_id)
    posts = posts.all()
    return render_template("posts.html", posts=posts)

@app.route("/post/<int:post_id>/edit", methods=["GET"])
def edit_post_get(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_post_post(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    # if there's a title post the new title AND If there's a content post the new content
    title=request.form["title"]
    # was content=mistune.markdown(request.form["content"]) but was seeing html tags in editing
    content=request.form["content"]
    session.query(Post).filter(Post.id == post_id).update(
         {"title":title, "content":content} )
    session.commit()
    # return render_template("edit_post.html", post=post)\
    return redirect(url_for("posts"))

@app.route("/post/<int:post_id>/delete", methods=["GET"])
def delete_get(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    return render_template("delete_post.html", post=post)

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    session.query(Post).filter(Post.id == post_id).delete(synchronize_session='evaluate')
    session.commit()
    return redirect(url_for("posts"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from models import User

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for(login_get))
    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))
