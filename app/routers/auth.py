from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordBearer, 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..import database, schemas, utils, models, oauth2


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    if not utils.verify(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    # create token
    # Return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}