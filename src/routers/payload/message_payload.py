from pydantic.fields import Field
from pydantic.main import BaseModel


class MessagePayload(BaseModel):
    firstname: str = Field(min_length=1)
    lastname: str = Field(min_length=1)
    age: int = Field(gt=0)
    weight: float = Field(gt=0)
