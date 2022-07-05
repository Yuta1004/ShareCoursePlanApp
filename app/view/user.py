from flask import session, request, render_template, Blueprint

from db.subject import get_classes_taking, get_classes_completed


route_user = Blueprint("user", __name__, url_prefix="/user")


@route_user.route("/")
def user():
    viewing_user = session["id"]
    taking_classes = get_classes_taking(viewing_user)
    completed_classes = get_classes_completed(viewing_user)
    return render_template("user.html", session=session, viewing_user=viewing_user, taking_classes=taking_classes, completed_classes=completed_classes)
