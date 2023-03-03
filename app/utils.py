from functools import lru_cache
from datetime import datetime, timedelta
from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt
import os

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


ACCESS_TOKEN_EXPIRES_IN = 30
ALGORITHM = 'HS256'
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)

    to_encode.update({'exp': expires_delta})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
