import json

from core import Webserver, HTTPRequest
from utils import load_page, redirect, parse_parameters
from utils.auth import create_user, protected
from utils.database import Database

server = Webserver()
db = Database("users.db")
db.setup()


@server.route("/", allowed_methods=["GET"])
def index(request: HTTPRequest):
    return load_page("index.html")

@server.route("/test-protected", allowed_methods=["GET"])
@protected()
def test_protected(request: HTTPRequest):
    server.logger.debug("Test protected called")
    return "<h1>This is a protected page</h1>"


@server.route("/test-redirect", allowed_methods=["GET"])
def test_redirect(request: HTTPRequest):
    return redirect("/")


@server.route("/signup", allowed_methods=["GET", "POST"])
def register(request: HTTPRequest):
    if request.method == "GET":
        if request.cookies.get("token"):
            return redirect("/dashboard")
        return load_page("signup.html")
    elif request.method == "POST":
        return create_user(*parse_parameters(request.body).values())

server.run("localhost", 8080)
