from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: constr(min_length=8)
    password_confirm: str
    role: str = 'user'
    verified: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(Token):
    name: str | None = None
    email: EmailStr | None = None
    role: str | None = None


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime


class FilteredUserResponse(UserBase):
    id: uuid.UUID


class ImageBase(BaseModel):
    title: str
    user_id: uuid.UUID

    class Config:
        orm_mode = True


class UploadImage(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: uuid.UUID
    user: FilteredUserResponse
    uploaded_at: datetime


class UpdateImage(BaseModel):
    title: str
    user_id: uuid.UUID | None = None

    class Config:
        orm_mode = True


class ListImageResponse(BaseModel):
    images: list[ImageResponse]
