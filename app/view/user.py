from flask import Blueprint


route_user = Blueprint("user", __name__, url_prefix="/user")


@route_user.route("/")
def user():
    return "User Page"
