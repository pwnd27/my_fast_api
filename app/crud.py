from sqlalchemy.orm import Session
from pydantic import EmailStr
from . import models, schemas
from app.utils import get_hashed_password


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.CreateUser):
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
