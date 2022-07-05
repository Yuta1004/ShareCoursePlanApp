from flask import session, request, render_template, Blueprint

from db.post import get_posts


route_top = Blueprint("top", __name__, url_prefix="/")


@route_top.route("/")
def index():
    page = 1
    try:
        page = int(request.args["page"])
    except:
        pass
    posts = get_posts(page)
    return render_template("index.html", session=session, page=page, posts=posts)
