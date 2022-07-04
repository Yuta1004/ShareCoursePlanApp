from flask import Blueprint


route_post = Blueprint("post", __name__, url_prefix="/post")


@route_post.route("/")
def post():
    return "Post Page"


@route_post.route("/detail")
def detail():
    return "Post Page"
