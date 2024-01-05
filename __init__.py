import logging
import os

from .server import Webserver
from .message import HTTPRequest, parse_message, HTTPResponse


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


status_messages = {
    200: "OK",
    404: "Not Found",
    405: "Method Not Allowed",
}


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
