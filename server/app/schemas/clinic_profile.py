"""
Clinic Profile Pydantic schemas for request/response validation.

This module defines Pydantic models for clinic profile-related API operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator, field_serializer


class ClinicProfileBase(BaseModel):
    """Base Clinic Profile schema with common fields."""
    
    clinic_name: str = Field(..., min_length=1, max_length=200, description="Official clinic name")
    license_number: str = Field(..., min_length=1, max_length=100, description="Business license number")
    address: str = Field(..., min_length=1, description="Full clinic address")
    phone: str = Field(..., min_length=10, max_length=20, description="Clinic contact phone")
    email: EmailStr = Field(..., description="Clinic contact email")
    operating_hours: Optional[dict] = Field(default_factory=dict, description="Operating schedule")
    services_offered: Optional[dict] = Field(default_factory=dict, description="Services provided")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "clinic_name": "Happy Pets Veterinary Clinic",
                "license_number": "VET-2023-12345",
                "address": "123 Main St, Springfield, IL 62701",
                "phone": "+1-555-123-4567",
                "email": "contact@happypetsvet.com",
                "operating_hours": {
                    "monday": "9:00 AM - 6:00 PM",
                    "tuesday": "9:00 AM - 6:00 PM",
                    "wednesday": "9:00 AM - 6:00 PM",
                    "thursday": "9:00 AM - 6:00 PM",
                    "friday": "9:00 AM - 6:00 PM",
                    "saturday": "10:00 AM - 4:00 PM",
                    "sunday": "Closed"
                },
                "services_offered": {
                    "general_checkup": True,
                    "emergency_care": True,
                    "surgery": True,
                    "dental": True,
                    "grooming": False
                }
            }
        }
    )


class ClinicProfileCreate(ClinicProfileBase):
    """Schema for creating a new clinic profile."""
    
    user_id: str = Field(..., description="User ID of the clinic owner/admin")
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        """Validate user_id is a valid UUID string."""
        from uuid import UUID
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError('user_id must be a valid UUID')


class ClinicProfileUpdate(BaseModel):
    """Schema for updating a clinic profile."""
    
    clinic_name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = Field(None, min_length=1)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    operating_hours: Optional[dict] = None
    services_offered: Optional[dict] = None
    is_active: Optional[bool] = None


class ClinicProfileResponse(ClinicProfileBase):
    """Schema for clinic profile response."""
    
    id: UUID = Field(..., description="Clinic profile ID")
    user_id: UUID = Field(..., description="User ID of the clinic owner")
    is_verified: bool = Field(..., description="Whether clinic is verified")
    is_active: bool = Field(..., description="Whether clinic is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    @field_serializer('id', 'user_id')
    def serialize_uuid(self, value: UUID) -> str:
        """Serialize UUID to string for JSON response."""
        return str(value)
    
    model_config = ConfigDict(from_attributes=True)

