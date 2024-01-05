import logging
import os

from .server import Webserver
from .models import HTTPRequest, HTTPResponse


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


status_messages = {
    200: "OK",
    404: "Not Found",
    405: "Method Not Allowed",
}
    
    
def parse_message(message: bytes) -> HTTPResponse:
    """Parse HTTP message."""
    lines = message.split(b"\r\n")
    method, path, version = [line.decode().strip("\r\n") for line in lines[0].split(b" ")]
    headers = {}
    body = b""
    for line in lines[1:]:
        if line == b"":
            body = lines[-1]
            break
        key, value = line.split(b": ")
        headers[key] = value
    return HTTPRequest(method, path, version, headers, body)


def build_response(status_code: int, headers: dict = None, body: bytes = None) -> bytes:
    """Builds a HTTP response.

    Args:
        status_code (int): HTTP status code
        headers (dict, optional): HTTP headers. Defaults to None.
        body (bytes, optional): HTTP body. Defaults to None.

    Returns:
        bytes: HTTP response
    """
    headers = headers or {}
    body = body or ""
    msg = HTTPResponse(status_code, status_messages[status_code], headers, body)
    return msg


def load_page(path: str) -> str:
    """Loads the HTML data from a file from the `html` folder.

    Args:
        path (str): Path to the HTML file to load

    Returns:
        str: HTML data
    """
    html_path = os.path.join(os.path.dirname(__file__), "../html")
    try:
        with open(f"{html_path}/{path}", "r") as f:
            logging.debug(f"Loading page ../html/{path}")
            return build_response(200, {"Content-Type": "text/html"}, f.read())
    except FileNotFoundError:
        return build_response(404)
