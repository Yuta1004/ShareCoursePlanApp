from flask import Blueprint


route_subject = Blueprint("subject", __name__, url_prefix="/subject")


@route_subject.route("/add")
def subject_add():
    return "Subject Add Page"


@route_subject.route("/remove")
def subject_remove():
    return "Subject Remove Page"


@route_subject.route("/csv")
def subject_csv():
    return "Subject CSV Page"
