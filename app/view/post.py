from flask import session, request, render_template, Blueprint

from db.post import save_post, get_post, get_replies


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
    post_id = request.args.get("id", "")
    result, post = get_post(post_id)
    replies = get_replies(post_id)
    if not result:
        return render_template("post_detail.html", session=session, warning_message="表示できる投稿がありません")
    return render_template("post_detail.html", session=session, post=post, replies=replies)
