from .. import schemas,models,oauth2
from fastapi import FastAPI, Response , status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)
@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(payload: schemas.PostCreate,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING *",(payload.title,payload.content))
    # new_post = cursor.fetchone()
    # connection.commit()
    print(user_id)
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

@router.get("/{post_id}",response_model=schemas.Post)
def get_post(post_id: int,response: Response,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s",(str(post_id)))
    # post = cursor.fetchone()
    # print(post)
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    return  post
    

@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,response: Response,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # for post in my_posts:
    #     if post["id"] == post_id:
    #         my_posts.remove(post)
    #         return Response(status_code=status.HTTP_204_NO_CONTENT)
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")

@router.put("/{post_id}",response_model=schemas.Post)
def update_post(post_id: int,payload: schemas.PostCreate,response: Response,db: Session = Depends(get_db)):
        # for post in my_posts:
    #     if post["id"] == post_id:
    #         post["title"] = payload.title
    #         post["content"] = payload.content
    #         post["published"] = payload.published
    #         post["rating"] = payload.rating
    #         return {"data": post}
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first():
        post.update(payload.model_dump())
        db.commit()
        return post.first()
    raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
