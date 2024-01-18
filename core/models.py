from dataclasses import dataclass

from utils import get_cookies


@dataclass
class HTTPRequest:
    """HTTP Request model."""
    method: str
    path: str
    version: str
    headers: dict
    body: bytes
    source: tuple = None
    cookies: dict = None

    def __post_init__(self):
        self.cookies = get_cookies(self.headers)


@dataclass
class HTTPResponse:
    """HTTP Response model."""
    status_code: int
    status_reason: str
    headers: dict
    body: bytes | str = None

    def __str__(self):
        headers_str = "\r\n".join(f"{header}: {value}" for header, value in self.headers.items())
        return f"HTTP/1.1 {self.status_code} {self.status_reason}\r\n{headers_str}\r\n\r\n{self.body if self.body else ''}"

    def __bytes__(self):
        return str(self).encode()
