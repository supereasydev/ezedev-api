from typing import Optional

from pydantic.fields import Field
from pydantic.main import BaseModel


class UserPayload(BaseModel):
    firstname: Optional[str] = Field(max_length=64)
    lastname: Optional[str] = Field(max_length=64)
