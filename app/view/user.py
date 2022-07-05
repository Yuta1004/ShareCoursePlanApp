from flask import session, redirect, request, render_template, Blueprint

from db.user import get_user_info
from db.settings import get_visibility
from db.subject import set_grade, get_classes_taking, get_classes_completed


route_user = Blueprint("user", __name__, url_prefix="/user")


@route_user.route("/", methods=["GET"])
def user_get():
    user_exists, user_info = get_user_info(request.args.get("id", session["id"]))
    viewing_is_owner = user_info["user_id"] == session["id"]
    visibility = get_visibility(user_info["user_id"])

    taking_classes = get_classes_taking(user_info["user_id"])
    completed_classes = get_classes_completed(user_info["user_id"])

    return render_template("user.html", session=session, user_exists=user_exists, user_info=user_info,
                           viewing_is_owner=viewing_is_owner, visibility=visibility,
                           taking_classes=taking_classes, completed_classes=completed_classes)


@route_user.route("/", methods=["POST"])
def user_post():
    for class_id, grade in request.form.items():
        if grade != "":
            set_grade(session["id"], class_id, grade)
    return redirect("/user")
