from fastapi.security.oauth2 import  OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2


router = APIRouter(tags=["Authetication"])
 
@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    email = db.query(models.User).filter(models.User.email == user_credentials.username).first()  
    
    if not email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, email.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":email.id})
    
     
    return {"access_token" : access_token, "token_type": "bearer" }    
