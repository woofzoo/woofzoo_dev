"""
Family Pydantic schemas for request/response validation.

This module defines Pydantic models for family-related API operations.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.models.family_member import AccessLevel


class FamilyBase(BaseModel):
    """Base Family schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Family name")
    description: Optional[str] = Field(None, max_length=500, description="Family description")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Smith Family",
                "description": "Our beloved pets family"
            }
        }
    )


class FamilyCreate(FamilyBase):
    """Schema for creating a new family."""
    pass


class FamilyUpdate(BaseModel):
    """Schema for updating an existing family."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Family name")
    description: Optional[str] = Field(None, max_length=500, description="Family description")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Family Name",
                "description": "Updated family description"
            }
        }
    )


class FamilyResponse(FamilyBase):
    """Schema for family response."""
    
    id: str = Field(..., description="Family unique identifier")
    owner_id: str = Field(..., description="Family owner's unique identifier")
    created_at: datetime = Field(..., description="Family creation timestamp")
    updated_at: datetime = Field(..., description="Family last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Smith Family",
                "description": "Our beloved pets family",
                "owner_id": "123e4567-e89b-12d3-a456-426614174001",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
    )


class FamilyMemberBase(BaseModel):
    """Base Family Member schema with common fields."""
    
    user_id: str = Field(..., description="User's unique identifier")
    access_level: AccessLevel = Field(..., description="Member's access level")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "access_level": "MEMBER"
            }
        }
    )


class FamilyMemberCreate(FamilyMemberBase):
    """Schema for adding a family member."""
    pass


class FamilyMemberUpdate(BaseModel):
    """Schema for updating a family member."""
    
    access_level: AccessLevel = Field(..., description="Member's access level")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_level": "ADMIN"
            }
        }
    )


class FamilyMemberResponse(FamilyMemberBase):
    """Schema for family member response."""
    
    id: str = Field(..., description="Family member unique identifier")
    family_id: str = Field(..., description="Family's unique identifier")
    user_email: str = Field(..., description="User's email address")
    user_name: str = Field(..., description="User's full name")
    joined_at: datetime = Field(..., description="Member join timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "family_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "user_email": "john.doe@example.com",
                "user_name": "John Doe",
                "access_level": "MEMBER",
                "joined_at": "2024-01-01T12:00:00Z"
            }
        }
    )


class FamilyInvitationBase(BaseModel):
    """Base Family Invitation schema with common fields."""
    
    invited_email: str = Field(..., description="Invitee's email address")
    invited_name: Optional[str] = Field(None, description="Invitee's name (optional, will be extracted from email if not provided)")
    access_level: AccessLevel = Field(..., description="Invited access level")
    message: Optional[str] = Field(None, max_length=500, description="Invitation message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invited_email": "jane.doe@example.com",
                "invited_name": "Jane Doe",
                "access_level": "MEMBER",
                "message": "Join our family to help care for our pets!"
            }
        }
    )


class FamilyInvitationCreate(FamilyInvitationBase):
    """Schema for creating a family invitation."""
    pass


class FamilyInvitationResponse(FamilyInvitationBase):
    """Schema for family invitation response."""
    
    id: str = Field(..., description="Invitation unique identifier")
    family_id: str = Field(..., description="Family's unique identifier")
    invited_by: str = Field(..., description="Inviter's unique identifier")
    status: str = Field(..., description="Invitation status")
    expires_at: datetime = Field(..., description="Invitation expiration timestamp")
    created_at: datetime = Field(..., description="Invitation creation timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174003",
                "family_id": "123e4567-e89b-12d3-a456-426614174000",
                "invited_email": "jane.doe@example.com",
                "access_level": "MEMBER",
                "message": "Join our family to help care for our pets!",
                "invited_by": "123e4567-e89b-12d3-a456-426614174001",
                "status": "PENDING",
                "expires_at": "2024-01-11T12:00:00Z",
                "created_at": "2024-01-01T12:00:00Z"
            }
        }
    )


class FamilyInvitationAccept(BaseModel):
    """Schema for accepting a family invitation."""
    
    token: str = Field(..., description="Invitation token")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "inv_1234567890abcdef"
            }
        }
    )


class FamilyListResponse(BaseModel):
    """Schema for list of families response."""
    
    families: List[FamilyResponse] = Field(..., description="List of families")
    total: int = Field(..., description="Total number of families")


class FamilyMemberListResponse(BaseModel):
    """Schema for list of family members response."""
    
    members: List[FamilyMemberResponse] = Field(..., description="List of family members")
    total: int = Field(..., description="Total number of members")


class FamilyInvitationListResponse(BaseModel):
    """Schema for list of family invitations response."""
    
    invitations: List[FamilyInvitationResponse] = Field(..., description="List of invitations")
    total: int = Field(..., description="Total number of invitations")
