import logging
from typing import List
from uuid import UUID

from src.persistence.models.user_model import UserModel
from src.persistence.repository.user_repository import UserRepository
from src.routers.payload.user_payload import UserPayload
from src.services.results.user_result import UserResult

logger = logging.getLogger(__name__)


class UserService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserService()
        return cls._instance

    def __init__(self):
        self.__user_repository = UserRepository.get_instance()

    async def get_user(self, id) -> UserResult:
        user_model = await self.__user_repository.get_by_id(id)
        if not user_model:
            raise Exception("User not found")
        return UserResult(user_model)

    async def get_users(self) -> List[UserResult]:
        user_models = await self.__user_repository.get_all_by_deleted_false()
        return [UserResult(user_model) for user_model in user_models]

    async def create_user(self, user_dto: UserPayload) -> UserResult:
        user_model = UserModel().fill(user_dto)
        return UserResult(await self.__user_repository.create(user_model))

    async def update_user(self, user_dto: UserPayload, id: UUID):
        user_model = await self.__user_repository.get_by_id(id)
        if not user_model:
            raise Exception("User not found")
        return UserResult(await self.__user_repository.update(user_model.fill(user_dto)))

    async def delete_user(self, id: UUID):
        user_model = await self.__user_repository.get_by_id(id)
        if not user_model:
            raise Exception("User not found")
        user_model.deleted = True
        return UserResult(await self.__user_repository.update(user_model))
