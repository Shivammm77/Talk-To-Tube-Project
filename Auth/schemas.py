from pydantic import BaseModel

class UserBase(BaseModel):
    username:str
class Usercreate(UserBase):
    password:str
    email : str
class UserResponse(UserBase):
    id:int    

    class Config:
        orm_mode = True