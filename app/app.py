from flask import session, request, redirect, Flask

from view.top import route_top
from view.auth import route_auth
from view.post import route_post
from view.settings import route_settings
from view.subject import route_subject
from view.user import route_user


DONT_NEEDS_LOGIN_URLS = ["/", "/auth/login", "/auth/register"]


app = Flask(__name__)
app.config["SECRET_KEY"] = "db1app"
app.config["MAX_CONTENT_LENGTH"] = 4*1024*1024
app.register_blueprint(route_top)
app.register_blueprint(route_auth)
app.register_blueprint(route_post)
app.register_blueprint(route_settings)
app.register_blueprint(route_subject)
app.register_blueprint(route_user)


@app.before_request
def before_request():
    if "logined" not in session.keys():
        session["logined"] = False
        session["is_admin"] = False
        session["name"] = ""

    needs_login = True not in [request.path == url for url in DONT_NEEDS_LOGIN_URLS]
    if needs_login and not session["logined"]:
        return redirect("/auth/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000)
