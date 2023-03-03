from sqlalchemy.orm import Session
from pydantic import EmailStr
import models
import schemas
from utils import get_hashed_password


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.CreateUser):
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_images(db: Session):
    images = db.query(models.Image).all()
    return images
