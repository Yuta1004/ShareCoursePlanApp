from flask import session, request, redirect, render_template, Blueprint

from db import auth


route_auth = Blueprint("auth", __name__, url_prefix="/auth")


@route_auth.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html", session=session)


@route_auth.route("/register", methods=["POST"])
def register_post():
    if request.form["password"] != request.form["password2"]:
        return render_template("register.html", session=session, warning_message="確認用パスワードが一致しません")

    result, user_id, user_name, is_admin = auth.register(request.form["name"], request.form["email"], request.form["password"])
    if result:
        session["logined"] = True
        session["is_admin"] = is_admin
        session["id"] = user_id
        session["name"] = user_name
        return redirect("/")
    return render_template("register.html", session=session, warning_message="全ての入力欄に情報を入力して下さい")


@route_auth.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html", session=session)


@route_auth.route("/login", methods=["POST"])
def login_post():
    result, user_id, user_name, is_admin = auth.login(request.form["email"], request.form["password"])
    if result:
        session["logined"] = True
        session["is_admin"] = is_admin
        session["id"] = user_id
        session["name"] = user_name
        return redirect("/")
    return render_template("login.html", session=session, warning_message="ログイン情報に誤りがあります")


@route_auth.route("/logout", methods=["GET"])
def logout_get():
    return render_template("logout.html", session=session)


@route_auth.route("/logout", methods=["POST"])
def logout_post():
    del session["logined"]
    del session["is_admin"]
    del session["id"]
    del session["name"]
    return redirect("/")
