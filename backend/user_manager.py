import uuid
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from models import User


async def get_user_db() -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    async with SessionLocal() as session:
        user_db = SQLAlchemyUserDatabase(session, User)  
        yield user_db


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    user_db_model = User
    async def on_after_register(self, user: User, request=None):
        print(f"User {user.email} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
