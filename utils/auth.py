import sqlite3
import hashlib
import uuid

from utils.database import Database
from utils import build_response


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
        "INSERT INTO `system_users` VALUES (?, ?, ?)", (username, password, new_token.hex)
    )
    conn.commit()
    return build_response(200, headers={
        "Set-Cookie": f"token={new_token}",
        "Location": "/"})


def auth_user(username: str, password: str) -> bytes:
    """Authenticate a user.

    Args:
        username (str): Username
        password (str): Password

    Returns:
        bytes: Corresponding HTTP response
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM `system_users` WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        if compare_passwords(password, result[1]):
            new_token = uuid.uuid4().hex
            c.execute("UPDATE `system_users` SET `token`=? WHERE `username`=?", (new_token, username))
            return build_response(301, headers={"Set-Cookie": f"token={new_token}", "Location": "/"})
    return build_response(401)


def protected() -> callable:
    def decorator(func: callable) -> callable:
        def wrapper(*args, **kwargs):
            cookies = args[0].cookies
            if cookies.get('token'):
                db = Database("users.db")
                if not db.validate_token(cookies["token"]):
                    return b"HTTP/1.1 403 Forbidden\r\n\r\n"
            else:
                return b"HTTP/1.1 401 Unauthorized\r\n\r\n"
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deauth_user():
    return b"HTTP/1.1 301 Moved Permanently\r\nSet-Cookie: token=; Max-Age=0\r\nLocation: /\r\n\r\n"
