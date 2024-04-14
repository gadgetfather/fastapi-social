from fastapi import FastAPI, Response , status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import oauth2
from app.database import get_db
from .. import models,schemas
router = APIRouter(
    prefix="/api/votes",
    tags=["votes"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def create_vote(vote:schemas.Vote ,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
        post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
        vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == int(user_id.id))
        found_vote = vote_query.first()
        if(vote.direction == 1):
            if found_vote:
                  raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="You have already upvoted this post")
            vote = models.Votes(post_id=vote.post_id,user_id=int(user_id.id))
            db.add(vote)
            db.commit()
            db.refresh(vote)
            return {"message":"Upvoted successfully"}

        else: 
              if not found_vote:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You have not upvoted this post")
              vote_query.delete(synchronize_session=False)
              db.commit()
              return {"message":"Downvoted successfully"}
              