import os
import logging
import socket

from core import HTTPRequest, HTTPResponse


status_messages = {
    200: "OK",
    301: "Moved Permanently",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
    501: "Not Implemented",
}


def parse_message(message: bytes, sender: socket.socket, sender_addr: tuple) -> HTTPRequest:
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
    return HTTPRequest(method, path, version, headers, body, (sender, sender_addr))


def build_response(status_code: int, headers: dict = None, body: bytes | str = "") -> bytes:
    """Builds a HTTP response.

    Args:
        status_code (int): HTTP status code
        headers (dict, optional): HTTP headers. Defaults to None.
        body (bytes, optional): HTTP body. Defaults to None.

    Returns:
        bytes: HTTP response
    """
    if headers is None:
        headers = dict()
    headers = dict(headers, **{"Content-Length": len(body), "Server": "Webserver"})
    msg = HTTPResponse(status_code, status_messages[status_code], headers, body)
    return bytes(msg)


def load_page(path: str) -> bytes:
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
            return build_response(status_code=200, headers={"Content-Type": "text/html"}, body=f.read())
    except FileNotFoundError:
        return build_response(404)
    

def redirect(location: str) -> bytes:
    """Redirects to a location.

    Args:
        location (str): Location to redirect to

    Returns:
        bytes: HTTP response
    """
    return build_response(301, headers={"Location": location})


def parse_parameters(parameters: str | bytes) -> dict:
    """Parse parameters from a string or bytes.

    Args:
        parameters (str | bytes): Parameters to parse

    Returns:
        dict: Parameters
    """
    if isinstance(parameters, bytes):
        parameters = parameters.decode()
    return {parameter.split("=")[0]: parameter.split("=")[1] for parameter in parameters.split("&")}


def get_cookies(headers: dict) -> dict:
    """Parse cookies from headers.

    Args:
        headers (dict): HTTP headers

    Returns:
        dict: Cookies
    """
    return {cookie.decode().split("=")[0]: cookie.decode().split("=")[1] for cookie in headers.get(b"Cookie", b"").split(b";") if cookie != b""}
