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