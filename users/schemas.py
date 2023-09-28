from pydantic import BaseModel, EmailStr
from datetime import datetime


class BaseUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    
class User(BaseUser):
    id: int
    registered_at: datetime