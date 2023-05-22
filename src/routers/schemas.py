from typing import Optional
from uuid import UUID

from pydantic.main import BaseModel


class UserSchema(BaseModel):
    id: UUID
    firstname: Optional[str]
    lastname: Optional[str]
