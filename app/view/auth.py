from flask import Blueprint


route_auth = Blueprint("auth", __name__, url_prefix="/auth")


@route_auth.route("/register")
def register():
    return "Register Page"


@route_auth.route("/login")
def login():
    return "Login Page"


@route_auth.route("/logout")
def logout():
    return "Logout Page"
