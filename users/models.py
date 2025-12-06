from sqlalchemy import Boolean , Column ,  Integer , String
from sqlalchemy.ext.declarative import declarative_base
from Auth.database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer  , primary_key=True , index=True)
    username = Column(String , unique = True , index=True)
    hashed_password = Column(String)
    password = Column(String)
    email = Column(String , unique=True)
    is_active = Column(Boolean , default=True)