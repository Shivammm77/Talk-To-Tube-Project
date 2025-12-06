# from passlib.context import CryptContext
# import jwt
# from jwt.exceptions import InvalidTokenError
# from datetime import datetime ,  timedelta
# SECRET_KEY = "Shivamki"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# def verify_password(plain_password :str , hashed_password:str):
#     return pwd_context.verify(plain_password , hashed_password)
# def get_password_hash(password:str):
#     return pwd_context.hash(password)
# def create_access_token(data: dict  , expires_delta : timedelta| None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(datetime.timezone.utc)+ expires_delta
#     else:
#         expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv("secret")
SECRET_KEY = key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    # bcrypt allows max 72 bytes → safe for all normal passwords
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

