from flask_bcrypt import Bcrypt

from app.core import app

bcrypt = Bcrypt(app)


def hash_password(password: str) -> str:
    password = password.encode()
    hashed_password = bcrypt.generate_password_hash(password)
    hashed_password = hashed_password.decode()
    return hashed_password


def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(hashed_password, password)
