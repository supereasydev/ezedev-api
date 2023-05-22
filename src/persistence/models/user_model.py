from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Integer

from src.persistence.models.base_models import TimedBaseModel


class UserModel(SQLAlchemyBaseUserTable[int], TimedBaseModel):
    firstname = Column(String(256), nullable=False)
    lastname = Column(String(256))
    age = Column(Integer)
