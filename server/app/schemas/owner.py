"""
Owner Pydantic schemas for request/response validation.

This module defines Pydantic models for owner-related API operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class OwnerBase(BaseModel):
    """Base Owner schema with common fields."""
    
    phone_number: str = Field(..., min_length=10, max_length=15, description="Owner's phone number")
    name: str = Field(..., min_length=1, max_length=100, description="Owner's full name")
    email: Optional[str] = Field(None, max_length=100, description="Owner's email address")
    address: Optional[str] = Field(None, description="Owner's address")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone_number": "+1234567890",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "address": "123 Main St, City, State 12345"
            }
        }
    )


class OwnerCreate(OwnerBase):
    """Schema for creating a new owner."""
    pass


class OwnerUpdate(BaseModel):
    """Schema for updating an existing owner."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Owner's full name")
    email: Optional[str] = Field(None, max_length=100, description="Owner's email address")
    address: Optional[str] = Field(None, description="Owner's address")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "address": "456 Oak Ave, City, State 12345"
            }
        }
    )


class OwnerResponse(OwnerBase):
    """Schema for owner response."""
    
    id: str = Field(..., description="Owner unique identifier")
    is_active: bool = Field(..., description="Owner account status")
    created_at: datetime = Field(..., description="Owner creation timestamp")
    updated_at: datetime = Field(..., description="Owner last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "phone_number": "+1234567890",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "address": "123 Main St, City, State 12345",
                "is_active": True,
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:00:00Z"
            }
        }
    )


class OwnerListResponse(BaseModel):
    """Schema for list of owners response."""
    
    owners: list[OwnerResponse] = Field(..., description="List of owners")
    total: int = Field(..., description="Total number of owners")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "owners": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "phone_number": "+1234567890",
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "address": "123 Main St, City, State 12345",
                        "is_active": True,
                        "created_at": "2025-01-01T12:00:00Z",
                        "updated_at": "2025-01-01T12:00:00Z"
                    }
                ],
                "total": 1
            }
        }
    )
