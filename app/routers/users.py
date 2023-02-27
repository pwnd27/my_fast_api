from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import schemas
import crud
from utils import create_access_token
from database import get_db
from dependencies import authenticate_user, get_current_user


router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, summary='Create new user', response_model=schemas.UserBase)
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Данная почта уже зарегистрирована')
    return crud.create_user(db=db, user=user)


@router.post('/token', summary='Create access token for user', response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неправильная почта или пароль',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me')
async def read_me(current_user: schemas.UserBase = Depends(get_current_user)):
    return current_user
