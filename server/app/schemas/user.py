"""
User schemas for API responses.

Defines Pydantic models for serializing user data in API responses.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from uuid import UUID


class UserResponse(BaseModel):
    """Schema representing a user in API responses."""

    id: int
    public_id: UUID = None
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    is_active: bool
    is_verified: bool
    personalization: dict = Field(default_factory=dict)
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for a paginated list of users."""

    users: List[UserResponse]
    total: int


