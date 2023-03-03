from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from crud import get_user_by_email
import schemas
from utils import verify_password, JWT_SECRET_KEY, ALGORITHM
from database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', scheme_name='JWT')


def authenticate_user(db: Session, email: EmailStr, password: str):
    user = get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Данные не валидны',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return schemas.UserBase(name=user.name, email=user.email)
