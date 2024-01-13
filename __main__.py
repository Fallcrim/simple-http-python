import json

from core import Webserver, HTTPRequest
from utils import load_page, redirect, parse_parameters, get_cookies
from utils.auth import create_user, protected, auth_user, deauth_user
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
def signup(request: HTTPRequest):
    if request.method == "GET":
        if get_cookies(request.headers).get("token"):
            return redirect("/")
        return load_page("signup.html")
    elif request.method == "POST":
        return create_user(*parse_parameters(request.body).values())


@server.route("/login", allowed_methods=["GET", "POST"])
def login(request: HTTPRequest):
    if request.method == "GET":
        if get_cookies(request.headers).get("token"):
            return redirect("/test-protected")
        return load_page("login.html")
    elif request.method == "POST":
        parameters = parse_parameters(request.body)
        if auth_user(parameters["username"], parameters["password"]):
            return redirect("/")
        else:
            return redirect("/login")


@server.route("/logout", allowed_methods=["GET"])
def logout(request: HTTPRequest):
    return deauth_user()

server.run("localhost", 8080)
