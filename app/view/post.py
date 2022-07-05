from flask import session, request, render_template, Blueprint

from db.post import save_post


route_post = Blueprint("post", __name__, url_prefix="/post")


@route_post.route("/", methods=["GET"])
def post_get():
    return render_template("post.html", session=session)


@route_post.route("/", methods=["POST"])
def post_post():
    result = save_post(session["id"], request.form["body"])
    if not result:
        return render_template("post.html", session=session, warning_message="全ての入力欄に入力してください")
    return render_template("post_success.html", session=session)


@route_post.route("/detail")
def detail():
    return render_template("post_detail.html", session=session)
