from typing import Optional

from pydantic.main import BaseModel


class PostResult(BaseModel):
    success: bool
    message: Optional[str]
    error: Optional[str]
