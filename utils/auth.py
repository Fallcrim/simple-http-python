import sqlite3
import hashlib
import uuid

from . import build_response
from utils.database import Database


def compare_passwords(password: str, hashed_password: str) -> bool:
    """Compare a password with a hashed password.

    Args:
        password (str): Password
        hashed_password (str): Hashed password

    Returns:
        bool: True if passwords match, False otherwise
    """
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password


def hash_password(password: str) -> str:
    """Hash a password.

    Args:
        password (str): Password

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username: str, password: str) -> bytes:
    """Create a user.

    Args:
        username (str): Username
        password (str): Password
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    new_token = uuid.uuid4()
    password = hash_password(password)

    c.execute(
        "INSERT INTO `system_users` VALUES (?, ?, ?)", (username, password, new_token)
    )
    conn.commit()
    return build_response(200, headers={
        "Set-Cookie": f"token={new_token}",
        "Location": "/dashboard"})


def auth_user(username: str, password: str) -> bool:
    """Authenticate a user.

    Args:
        username (str): Username
        password (str): Password

    Returns:
        bool: True if user is authenticated, False otherwise
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM `system_users` WHERE username=`?`", (username, password))
    if c.fetchone():
        if compare_passwords(password, c.fetchone()[1]):
            return True
    return False


def protected() -> callable:
    def decorator(func: callable) -> callable:
        def wrapper(*args, **kwargs):
            if not args[0].cookies.get(b"token"):
                return b"HTTP/1.1 401 Unauthorized\r\n\r\n"
            db = Database("users.db")
            if not db.validate_token(args[0].cookies[b"token"]):
                return b"HTTP/1.1 403 Forbidden\r\n\r\n"
            return func(*args, **kwargs)

        return wrapper

    return decorator
