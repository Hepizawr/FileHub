import typing as t
import uuid

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID
    username: str
    is_admin: bool


class File(BaseModel):
    id: uuid.UUID
    name: str
    format: str
    users: t.List[User]
