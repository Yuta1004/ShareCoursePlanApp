from flask import Blueprint


route_top = Blueprint("top", __name__, url_prefix="/")


@route_top.route("/")
def index():
    return "Index Page"
