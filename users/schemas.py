from pydantic import BaseModel
class UserBase(BaseModel):
    username : str
    
class Usercreate(UserBase):
    password:str
    email: str
class User(UserBase):
     id : int
     is_active : bool
     class config:
        orm_mode = True     