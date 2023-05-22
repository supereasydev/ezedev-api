from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserResult:
    id: UUID
    firstname: str
    lastname: str

    def __init__(self, model):
        self.id = model.id
        self.firstname = model.firstname
        self.lastname = model.lastname
