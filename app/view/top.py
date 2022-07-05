from flask import session, request, render_template, Blueprint

from db.post import get_posts, incr_like_count


route_top = Blueprint("top", __name__, url_prefix="/")


@route_top.route("/", methods=["GET"])
def index_get():
    page = 1
    try:
        page = int(request.args["page"])
    except:
        pass
    posts = get_posts(page)
    return render_template("index.html", session=session, page=page, posts=posts, like_count=[])


@route_top.route("/", methods=["POST"])
def index_post():
    incr_like_count(request.form["like"], session["id"])
    page = 1
    try:
        page = int(request.args["page"])
    except:
        pass
    posts = get_posts(page)
    return render_template("index.html", session=session, page=page, posts=posts, like_count=[])
