from flask import session, redirect, request, render_template, Blueprint

from db.subject import set_grade, get_classes_taking, get_classes_completed


route_user = Blueprint("user", __name__, url_prefix="/user")


@route_user.route("/", methods=["GET"])
def user_get():
    viewing_user = session["id"]
    taking_classes = get_classes_taking(viewing_user)
    completed_classes = get_classes_completed(viewing_user)
    return render_template("user.html", session=session, viewing_user=viewing_user, taking_classes=taking_classes, completed_classes=completed_classes)


@route_user.route("/", methods=["POST"])
def user_post():
    for class_id, grade in request.form.items():
        if grade != "":
            set_grade(session["id"], class_id, grade)
    return redirect("/user")
