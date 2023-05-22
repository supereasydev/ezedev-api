from datetime import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from src.persistence.database import Database


class BaseModel(Database.get_instance().db.Model):
    __abstract__ = True
    id = Column(UUID, primary_key=True, default=Database.get_instance().db.func.uuid_generate_v4())
    deleted = Column(Database.get_instance().db.Boolean, default=False, index=True)

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Database.get_instance().db.Column(Database.get_instance().db.DateTime(True),
                                                   server_default=Database.get_instance().db.func.now(),
                                                   default=datetime.utcnow)
    updated_at = Database.get_instance().db.Column(
        Database.get_instance().db.DateTime(True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=Database.get_instance().db.func.now(),
        index=True
    )
