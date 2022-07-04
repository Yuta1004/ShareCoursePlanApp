from flask import Blueprint


route_settings = Blueprint("settings", __name__, url_prefix="/settings")


@route_settings.route("/")
def settings():
    return "Settings Page"
