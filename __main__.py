from core import Webserver, HTTPRequest
from utils import load_page


server = Webserver()


@server.route("/", allowed_methods=["GET"])
def index(request: HTTPRequest):
    return load_page("index.html")

@server.route("/test-protected", allowed_methods=["GET"])
def test_protected(request: HTTPRequest):
    server.logger.debug("Test protected called")
    return "<h1>This is a protected page</h1>"


server.run("localhost", 8080)
