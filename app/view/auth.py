from flask import session, request, redirect, render_template, Blueprint

from db import auth


route_auth = Blueprint("auth", __name__, url_prefix="/auth")


@route_auth.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html", user=session["user"])


@route_auth.route("/register", methods=["POST"])
def register_post():
    if request.form["password"] != request.form["password2"]:
        return render_template("register.html", user=session["user"], warning_message="確認用パスワードが一致しません")

    result, user_id = auth.register(request.form["name"], request.form["email"], request.form["password"])
    if result:
        session["user"] = user_id
        return redirect("/")
    return render_template("register.html", user=session["user"], warning_message="全ての入力欄に情報を入力して下さい")


@route_auth.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html", user=session["user"])


@route_auth.route("/login", methods=["POST"])
def login_post():
    result, user_id = auth.login(request.form["email"], request.form["password"])
    if result:
        session["user"] = user_id
        return redirect("/")
    return render_template("login.html", user=session["user"], warning_message="ログイン情報に誤りがあります")


@route_auth.route("/logout", methods=["GET"])
def logout_get():
    return render_template("logout.html", user=session["user"])


@route_auth.route("/logout", methods=["POST"])
def logout_post():
    session["user"] = None
    return redirect("/")

