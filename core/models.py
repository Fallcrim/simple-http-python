from dataclasses import dataclass
import logging


@dataclass
class HTTPRequest:
    """HTTP Message."""
    method: str
    path: str
    version: str
    headers: dict
    body: bytes
    source: tuple = None


@dataclass
class HTTPResponse:
    """HTTP Response."""
    status_code: int
    status_reason: str
    headers: dict
    body: bytes | str = None

    def __str__(self):
        headers_str = "\r\n".join(f"{header}: {value}" for header, value in self.headers.items())
        return f"HTTP/1.1 {self.status_code} {self.status_reason}\r\n{headers_str}\r\n\r\n{self.body if self.body else ''}"

    def __bytes__(self):
        return str(self).encode()
