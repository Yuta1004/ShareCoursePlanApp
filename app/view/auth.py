from flask import render_template, Blueprint


route_auth = Blueprint("auth", __name__, url_prefix="/auth")


@route_auth.route("/register")
def register():
    return "Register Page"


@route_auth.route("/login")
def login():
    return render_template("login.html")


@route_auth.route("/logout")
def logout():
    return render_template("logout.html")
