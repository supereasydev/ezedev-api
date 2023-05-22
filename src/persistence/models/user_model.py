from sqlalchemy import sql, Column, String, BIGINT

from src.persistence.models.base_models import TimedBaseModel
from src.routers.payload.user_payload import UserPayload


class UserModel(TimedBaseModel):
    __tablename__ = 'users'
    query: sql.Select

    firstname = Column(String(256), nullable=False)
    lastname = Column(String(256))

    def fill(self, payload: UserPayload):
        self.firstname = payload.firstname
        self.lastname = payload.lastname
        return self
