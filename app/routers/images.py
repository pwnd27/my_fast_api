from datetime import datetime
import uuid

import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from database import get_db
from crud import get_images
from dependencies import get_current_user
# from app.oauth2 import require_user

router = APIRouter()


@router.get('/test', response_model=schemas.ListImageResponse)
def get_image(db: Session = Depends(get_db)):
    images = get_images(db=db)
    return images


# @router.get('/', response_model=schemas.ListImageResponse)
# def get_images(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '',
#                user_id: str = Depends(require_user)):
#     skip = (page - 1) * limit
#
#     images = db.query(models.Image).group_by(models.Image.id).filter\
#         (models.Image.title.contains(search)).limit(limit).offset(skip).all()
#     return {'status': 'success', 'results': len(images), 'images': images}
#
#
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ImageResponse)
def upload_image(image: schemas.UploadImage, db: Session = Depends(get_db),
                 user: schemas.UserBase = Depends(get_current_user)):
    image.user_id = uuid.UUID(user.id)
    new_image = models.Image(**image.dict())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image
#
#
# # @router.put('/{id}', response_model=schemas.ImageResponse)
# def update_image(id: str, image: schemas.UpdateImage, db: Session = Depends(get_db),
#                  user_id: str = Depends(require_user)):
#     image_query = db.query(models.Image).filter(models.Image.id == id)
#     updated_image = image_query.first()
#
#     if not updated_image:
#         raise HTTPException(status_code=status.HTTP_200_OK, detail=f'Изображение с таким id: {id} не существует')
#
#     if updated_image.user_id != uuid.UUID(user_id):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
#
#     image.user_id = user_id
#     image_query.update(image.dict(exclude_unset=True), synchronize_session=False)
#     db.commit()
#     return updated_image
#
#
# @router.get('/{id}')
# def get_image(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
#     image = db.query(models.Image).filter(models.Image.id == id).first()
#     if not image:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Изображение с таким id: {id} не существует')
#     return image
#
#
# @router.delete('/{id}')
# def delete_image(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
#     image_query = db.query(models.Image).filter(models.Image.id == id)
#     image = image_query.first()
#     if not image:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Изображение с таким id: {id} не существует')
#
#     if str(image.user_id) != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
#     image_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
