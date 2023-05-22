from sqlalchemy import Column, Boolean, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement='auto')
    deleted = Column(Boolean, default=False, index=True)


class TimedBaseModel(BaseModel):
    __abstract__ = True
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
