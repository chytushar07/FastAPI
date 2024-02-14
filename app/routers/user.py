from .. import models,schemas,utils
from fastapi import FastAPI, HTTPException , Response ,status ,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine ,SessionLocal, get_db
from typing import Optional,List

router =APIRouter(
    tags=['User']
)

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    user_search=db.query(models.User).filter(models.User.email==user.email)
    if user_search.first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"email already exist")


    hashed_password=new_user=utils.hash(user.password)
    user.password=hashed_password
    
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# @ suggest decorator
@router.get("/users/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user =db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
    return user