from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    user = "user"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Role 
    isactive: bool 

    class Config:
        from_attributes = True
