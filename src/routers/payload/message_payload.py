from pydantic import BaseModel


class MessagePayload(BaseModel):
    firstname: str
    lastname: str
    age: int
    weight: float
