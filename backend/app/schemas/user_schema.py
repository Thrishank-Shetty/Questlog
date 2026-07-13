from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username:str
    email:str
    password:str
    confirmpassword:str

class UserLogin(BaseModel):
    identifier:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    role:str
    is_active:bool
    created_at:datetime
