from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users.router.auth import get_auth_router
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
import uuid
from user_manager import get_user_manager
from models import User
import os
from config import settings
from pydantic import EmailStr, constr, Field, StringConstraints, field_validator
from typing import Annotated
import re 

JWT_SECRET = settings.JWT_SECRET

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

SECRET = JWT_SECRET

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend]
)
UsernameStr = Annotated[
    str,
    StringConstraints(
        pattern="^[a-zA-Z][a-zA-Z0-9]*$",
        min_length=3,
        max_length=20,
        strip_whitespace=True
    )
]

class BaseUserCreate(BaseUserCreate):
    username: UsernameStr
    email: EmailStr
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must have at least 8 characters.")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number.")
        return v
    
class UserRead(BaseUser):
    email: str
    username: str

    class Config:
        orm_mode = True
