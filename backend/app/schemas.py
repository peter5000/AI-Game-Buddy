from pydantic import BaseModel, Field, EmailStr, SecretStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr = Field(
        json_schema_extra={"format": "password"},
    )

class User(BaseModel):
    id: str
    user_id: str
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    identifier: str
    password: SecretStr = Field(
        json_schema_extra={"format": "password"},
    )