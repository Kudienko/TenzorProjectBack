from typing import Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models

from auth.database import CustomUser, get_user_db
from src.config import settings
from auth.schemas import UserCreate, UserRead

SECRET = settings.SECRET_M


class UserManager(IntegerIDMixin, BaseUserManager[CustomUser, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: CustomUser, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self, user_create: UserCreate, safe: bool = False, request: Optional[Request] = None
    ) -> UserRead:
        await self.validate_password(user_create.hashed_password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = user_create.dict(exclude_unset=True)
        user_dict["hashed_password"] = self.password_helper.hash(user_create.hashed_password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return UserRead.from_orm(created_user)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)