
from sqlalchemy import func
from .. import models,schemas,utils,oauth2
from fastapi import FastAPI, HTTPException , Response ,status ,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine ,SessionLocal, get_db
from typing import Optional,List


router =APIRouter(
    tags=['Posts']
    # prefix="/posts"
)

# @router.get("/posts",response_model=list[schemas.Post])
@router.get("/posts")
def get_posts(db: Session = Depends(get_db),Limit:int=3,skip:int=0,search:Optional[str]=''):
    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all() #from models file access Post
    results= db.query(models.Post,func.count(models.Post.id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()

    return posts
    # &skip=2 -skips post-Maintains pagination.
#   %20 is added instead of space incase to search str which has space



@router.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # new_post=models.Post(title=post.title,content=post.content,published=post.published) #Here we have limited fields how can we handle that-We create models for it.
    # print(**post.model_dump()) # uppack dict
    # print(current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.model_dump()) # Here we have limited fields how can we handle that-We create models for it.

    db.add(new_post)
    db.commit()
    db.refresh(new_post)# Retrive new_created_post
    # Here ORM will convert data into Dict

    return new_post



@router.get("/posts/{id}",response_model=schemas.Post) #Id represents path parameter
def get_post(id: int,db: Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user) ):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    # post=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() #Fetches all related post of logged in user

    # print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized requested action")
    
    return post
  

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post_query=db.query(models.Post).filter(models.Post.id==id) # This is a query to find post
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostBase,db: Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id) # This is a query to find post
    post=  post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized requested action")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()

