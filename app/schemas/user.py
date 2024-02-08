from pydantic import BaseModel, validator, SecretStr, EmailStr, StringConstraints
from typing import Annotated


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class BaseRole(BaseModel):
    name: str

    class Config:
        form_attributes = True

class Role(BaseRole):
    id: int

    class Config:
        form_attributes = True

class UserBase(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    email: EmailStr
    contact: str
    role_id: int

    @validator("username")
    def validate_username_no_spaces(cls, value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value
    
class User(UserBase):
    id: int

    class Config:
        form_attributes = True

class CreateUser(UserBase):
    password: SecretStr

    class Config:
        form_attributes = True