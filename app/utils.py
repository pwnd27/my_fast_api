from functools import lru_cache
from datetime import datetime, timedelta
from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt
import config


@lru_cache()
def get_settings():
    return config.Settings


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict, settings: config.Settings = Depends(get_settings)) -> str:
    to_encode = data.copy()
    expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)

    to_encode.update({'exp': expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt
