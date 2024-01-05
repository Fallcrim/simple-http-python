from dataclasses import dataclass


@dataclass
class HTTPRequest:
    """HTTP Message."""
    method: str
    path: str
    version: str
    headers: dict
    body: bytes
    
    
@dataclass
class HTTPResponse:
    """HTTP Response."""
    status_code: int
    status_reason: str
    headers: dict
    body: bytes
    
    
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