from .. import models, schemas, utils
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db







router= APIRouter(
    prefix="/user",
    tags=['Users']
)

#CREATE USER

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = utils.get_hashed_password(data.password)
    data.password = hashed_password
    
    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    

@router.get("/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db )):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User With {id} Not Found" )
    
    return user
    