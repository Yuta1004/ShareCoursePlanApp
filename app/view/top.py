from flask import session, request, render_template, Blueprint


route_top = Blueprint("top", __name__, url_prefix="/")


@route_top.route("/")
def index():
    page = 1
    try:
        page = int(request.args["page"])
    except:
        pass
    return render_template("index.html", user=session["user"], page=page, posts=[])
