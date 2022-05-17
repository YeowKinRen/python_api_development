from app import oauth2
from .. import models
from ..database import engine, get_db
from ..schemas import Vote
from sqlalchemy.orm import Session
from fastapi import Response, FastAPI, status, HTTPException, Depends, APIRouter
from .. import utils

router = APIRouter(
    prefix="/votes", 
    tags=['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)#, response_model=VoteResponse)
def create_vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{vote.post_id} does not exist")
    

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"messages":"success added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"vote does not exists")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"messages":"success delete"}