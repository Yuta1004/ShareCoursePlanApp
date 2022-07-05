import io

import pandas as pd
from flask import session, request, render_template, Blueprint
from werkzeug.datastructures import FileStorage

from db.subject import save_classes_from_csv


route_subject = Blueprint("subject", __name__, url_prefix="/subject")


@route_subject.route("/add")
def subject_add():
    return "Subject Add Page"


@route_subject.route("/remove")
def subject_remove():
    return "Subject Remove Page"


@route_subject.route("/csv", methods=["GET"])
def subject_csv_get():
    return render_template("csvload.html")


@route_subject.route("/csv", methods=["POST"])
def subject_csv_post():
    file = request.files.get("csvfile")
    if not isinstance(file, FileStorage) or file.content_type != "text/csv":
        return render_template("csvload.html", warning_message="CSV形式のファイルをアップロードしてください")

    try:
        csv = pd.read_csv(file, encoding="sjis")
        result, saved_classes = save_classes_from_csv(csv)
        if not result:
            raise Exception()
    except:
        return render_template("csvload.html", warning_message="KdBからダウンロードしたCSVファイルをアップロードしてください")

    return render_template("csvload_success.html", session=session, saved_classes=saved_classes)
