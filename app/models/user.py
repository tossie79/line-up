from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    """Base Model representing common user attributes."""

    email: str
    first_name: str
    last_name: str
    avatar: Optional[str] = None


class User(UserBase):
    """Response Model representing a user with an ID."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    """Response Model representing a paginated list of users."""

    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]

    model_config = ConfigDict(from_attributes=True)
