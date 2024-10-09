import bcrypt


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")
    return hashed_password.decode("utf-8")
