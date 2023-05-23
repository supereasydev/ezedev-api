import logging
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, exceptions, schemas
from sqlalchemy import select

from src.config import Config
from src.persistence.database import Database, get_user_db
from src.persistence.models.user_model import UserModel
from src.security.custom_credentials import OAuth2PasswordRequestCustomForm

database = Database.get_instance()
config = Config.get_instance()


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, int]):
    reset_password_token_secret = config.jwt_secret
    verification_token_secret = config.jwt_secret
    logger = logging.getLogger(__name__)

    async def on_after_register(self, user: UserModel, request: Optional[Request] = None):
        self.logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        self.logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        self.logger.info(f"Verification requested for user {user.id}. Verification token: {token}")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.get_by_phone(user_create.phone)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def authenticate(
            self, credentials: OAuth2PasswordRequestCustomForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following a phone and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_phone(credentials.phone)
            if user is None:
                raise exceptions.UserNotExists()
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def get_by_phone(self, phone: str) -> UserModel:
        """
        Get a user by its phone.

        :param phone: The user phone.
        :return: The user.
        """
        stmt = select(UserModel).where(UserModel.phone == phone)
        return (await self.user_db.session.execute(stmt)).unique().scalar_one_or_none()


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
