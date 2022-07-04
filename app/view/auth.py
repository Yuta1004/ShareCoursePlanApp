from flask import session, request, redirect, render_template, Blueprint

from db.auth import login


route_auth = Blueprint("auth", __name__, url_prefix="/auth")


@route_auth.route("/register")
def register():
    return "Register Page"


@route_auth.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@route_auth.route("/login", methods=["POST"])
def login_post():
    if login(request.form["userid"], request.form["password"]):
        session["userid"] = request.form["userid"]
        return redirect("/")
    return render_template("login.html", warning_message="ログイン情報に誤りがあります")


@route_auth.route("/logout")
def logout():
    return render_template("logout.html")
