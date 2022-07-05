from flask import session, request, render_template, Blueprint

from db.post import save_post, get_post, save_reply, get_replies, incr_like_count


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


@route_post.route("/detail", methods=["GET"])
def detail_get():
    post_id = request.args.get("id", "")
    result, post = get_post(post_id)
    replies = get_replies(post_id)
    if not result:
        return render_template("post_detail.html", session=session, warning_message="表示できる投稿がありません")
    return render_template("post_detail.html", session=session, post=post, replies=replies)


@route_post.route("/detail", methods=["POST"])
def detail_post():
    incr_like_count(request.form["like"], session["id"])
    post_id = request.args.get("id", "")
    result, post = get_post(post_id)
    replies = get_replies(post_id)
    if not result:
        return render_template("post_detail.html", session=session, warning_message="表示できる投稿がありません")
    return render_template("post_detail.html", session=session, post=post, replies=replies)


@route_post.route("/reply", methods=["POST"])
def reply_post():
    reply_to = request.form.get("id", "")
    result = save_reply(reply_to, session["id"], request.form["body"])
    if not result:
        _, post = get_post(reply_to)
        replies = get_replies(reply_to)
        return render_template("post_detail.html", session=session, post=post, replies=replies, reply_warning_message="全ての入力欄に入力してください")
    return render_template("post_reply_success.html", session=session)
