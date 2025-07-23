import uuid
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())) # Partition Key
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    identifier: str
    password: str