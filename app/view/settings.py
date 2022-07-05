from flask import session, render_template, Blueprint

from db.user import get_user_info
from db.settings import get_visibility


route_settings = Blueprint("settings", __name__, url_prefix="/settings")


@route_settings.route("/")
def settings():
    return render_template("settings.html", **load_settings(session["id"]))


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
