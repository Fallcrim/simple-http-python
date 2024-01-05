from . import Webserver, HTTPRequest, load_page


server = Webserver()


@server.route("/", allowed_methods=["GET"])
def index(request: HTTPRequest):
    server.logger.debug("Index called")
    return load_page("index.html")


server.run("localhost", 8080)
