from flask import render_template, Blueprint


route_post = Blueprint("post", __name__, url_prefix="/post")


@route_post.route("/")
def post():
    return render_template("post.html")


@route_post.route("/detail")
def detail():
    return render_template("post_detail.html")
