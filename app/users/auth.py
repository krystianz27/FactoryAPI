import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

# from jose import jwt # Mor Advanced encoding
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session  # Poprawny import

from app.db_connection import get_db_session
from app.users.models import User

# Zdefiniuj zmienne
SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Konfiguracja haszowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Funkcja do haszowania hasła
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Funkcja do weryfikacji hasła
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Funkcja do generowania tokenu JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # Użycie timezone.utc
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )  # Użycie timezone.utc
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Funkcja do weryfikacji tokenu i uzyskania aktualnego użytkownika
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise credentials_exception  # Użytkownik nie został znaleziony

    except jwt.PyJWTError:
        raise credentials_exception

    return user
