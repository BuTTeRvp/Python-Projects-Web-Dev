from typing import List
from .. import models, schemas
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db





router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#Postgres Without ORM ->
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="FastAPI", user="postgres", password="unotrick"
#                                 , cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("DataBase Connected!")
#         break
#     except Exception as err:
#         print("Connection to DB failed ")
#         print(err)
#         time.sleep(2)   

# @router.get("/")
# async def root():
#     return {"message": "Hello World"}


@router.get("/", response_model=List[schemas.PostResponse])                              # ---READ---
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)                 
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)     # ---CREATE---
def create_post(data: schemas.PostCreate, db: Session = Depends(get_db)):   
    #using SQL DIRECTLY 
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *"""
    #                ,(data.title,data.content,data.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    #using sql alchemy
    #new_post = models.Post(title=data.title, content=data.content, published=data.published)
    
    new_post = models.Post(**data.dict())          # new_post is a sql alchemy model 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post


@router.get('/{id}', response_model=schemas.PostResponse)    #!! GETS A SINGEL POST FROM ID !!  #{id} field -> path parameter
def get_post(id: int, db: Session = Depends(get_db)):  #id needs to be converted to integer ,default is string from request.
    
    # <1> using sql directly 
    
    # cursor.execute("""SELECT * FROM posts WHERE id= %s  """, (str(id)))
    # post = cursor.fetchone()
    
    # <2> using SQL ALCHEMY (ORM)
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"{id} not found")
    
    return  post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)   # ---DELETE--- 
def del_post(id: int, db: Session = Depends(get_db)):
    #<1> Direct SQL 
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    #<2> ORM -> SQL ALCHEMY
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)   # query 
    
    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} Not Found")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

      
@router.put("/{id}", response_model=schemas.PostResponse)                             # ---UPDATE---
def update_post(id: int, data : schemas.PostCreate, db: Session = Depends(get_db)):
    #<1> Postgres directly 
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id =%s RETURNING *""",
    #                (data.title, data.content, data.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    #<2> ORM sql alchemy
    
    update_post_query  = db.query(models.Post).filter(models.Post.id == id)
    post = update_post_query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} Not Found")
    
    update_post_query.update(data.dict(),synchronize_session=False)
    db.commit()
  
    return update_post_query.first()
