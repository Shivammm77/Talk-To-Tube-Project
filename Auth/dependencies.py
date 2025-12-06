from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError as JWTError
from sqlalchemy.orm import Session
from .utils import verify_password, get_password_hash, create_access_token , SECRET_KEY , ALGORITHM
from .models import TokenData 
from users.models import User
from .database import SessionLocal, engine, Base


o2auth = OAuth2PasswordBearer(tokenUrl="auth/token")
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()    
def get_user(db:Session , username:str):
    return db.query(User).filter(User.username == username).first()
def authenticate_user(db:Session , username : str , password:str):
    user = get_user(db , username)
    if not user : 
        return False
    if not verify_password(password , user.hashed_password):
        return False
    return user
def get_current_user(db:Session = Depends(get_db) , token :str =  Depends(o2auth)) :
    current_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED , 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, 
    )   
    try : 
        payload = jwt.decode(token , SECRET_KEY  , algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None : 
            raise current_exception
        token_data = TokenData(username = username)
    except JWTError:
        raise current_exception 
    user = get_user(db , username= token_data.username)
    if user is None:
       raise current_exception
    return user 