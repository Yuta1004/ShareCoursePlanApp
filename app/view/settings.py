from flask import session, request, render_template, Blueprint

from db.auth import update_password
from db.user import get_user_info, update_user_info
from db.settings import get_visibility, update_visibility


route_settings = Blueprint("settings", __name__, url_prefix="/settings")


@route_settings.route("/")
def settings():
    return render_template("settings.html", **load_settings(session["id"]))


@route_settings.route("/user", methods=["POST"])
def settings_user():
    result = update_user_info(session["id"], request.form["email"], request.form["name"])
    if not result:
        return render_template("settings.html", **load_settings(session["id"]), warning_message="全ての入力欄に入力してください")
    session["name"] = request.form["name"]
    return render_template("settings.html", **load_settings(session["id"]), success=True)


@route_settings.route("/password", methods=["POST"])
def settings_password():
    if request.form["password"] != request.form["password2"]:
        return render_template("settings.html", **load_settings(session["id"]), warning_message="確認用パスワードが一致しません")
    result = update_password(session["id"], request.form["password"])
    if not result:
        return render_template("settings.html", **load_settings(session["id"]), warning_message="8文字以上のパスワードを入力してください")
    return render_template("settings.html", **load_settings(session["id"]), success=True)


@route_settings.route("/visibility", methods=["POST"])
def settings_visibility():
    update_visibility(
        session["id"],
        "taking_class_is_public" in request.form.getlist("settings"),
        "complete_class_is_public" in request.form.getlist("settings"),
        "grade_is_public" in request.form.getlist("settings")
    )
    return render_template("settings.html", **load_settings(session["id"]), success=True)


def load_settings(user_id):
    settings = {}

    _, user_info = get_user_info(user_id)
    settings["email"] = user_info["email"]
    settings["name"] = user_info["name"]

    visiblity = get_visibility(user_id)
    settings["taking_class_is_public"] = visiblity["taking_class_is_public"]
    settings["complete_class_is_public"] = visiblity["complete_class_is_public"]
    settings["grade_is_public"] = visiblity["grade_is_public"]

    return settings
