"""
Pet Clinic Access Pydantic schemas for request/response validation.

This module defines Pydantic models for pet clinic access-related API operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer


class PetClinicAccessBase(BaseModel):
    """Base Pet Clinic Access schema with common fields."""
    
    purpose: Optional[str] = Field(None, max_length=200, description="Reason for visit")


class PetClinicAccessRequest(BaseModel):
    """Schema for requesting clinic access (generates OTP)."""
    
    pet_id: str = Field(..., description="Pet's ID")
    clinic_id: str = Field(..., description="Clinic's ID")
    purpose: Optional[str] = Field(None, max_length=200, description="Reason for visit")
    
    @field_validator('pet_id', 'clinic_id')
    @classmethod
    def validate_uuid_fields(cls, v, info):
        """Validate UUID fields."""
        from uuid import UUID
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError(f'{info.field_name} must be a valid UUID')
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174000",
                "clinic_id": "223e4567-e89b-12d3-a456-426614174000",
                "purpose": "Annual wellness checkup"
            }
        }
    )


class PetClinicAccessGrant(BaseModel):
    """Schema for granting clinic access (validates OTP)."""
    
    pet_id: str = Field(..., description="Pet's ID")
    clinic_id: str = Field(..., description="Clinic's ID")
    otp_code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")
    doctor_id: Optional[str] = Field(None, description="Assigned doctor's ID")
    access_duration_hours: int = Field(24, ge=1, le=168, description="Access duration in hours (default 24)")
    
    @field_validator('pet_id', 'clinic_id', 'doctor_id')
    @classmethod
    def validate_uuid_fields(cls, v, info):
        """Validate UUID fields."""
        if v is None:
            return v
        from uuid import UUID
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError(f'{info.field_name} must be a valid UUID')
    
    @field_validator('otp_code')
    @classmethod
    def validate_otp_code(cls, v):
        """Validate OTP code is numeric."""
        if not v.isdigit():
            raise ValueError('otp_code must be numeric')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174000",
                "clinic_id": "223e4567-e89b-12d3-a456-426614174000",
                "otp_code": "123456",
                "doctor_id": "323e4567-e89b-12d3-a456-426614174000",
                "access_duration_hours": 24
            }
        }
    )


class PetClinicAccessRevoke(BaseModel):
    """Schema for revoking clinic access."""
    
    access_id: str = Field(..., description="Access record ID to revoke")
    
    @field_validator('access_id')
    @classmethod
    def validate_access_id(cls, v):
        """Validate access_id is a valid UUID."""
        from uuid import UUID
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError('access_id must be a valid UUID')


class PetClinicAccessResponse(PetClinicAccessBase):
    """Schema for pet clinic access response."""
    
    id: UUID = Field(..., description="Access record ID")
    pet_id: UUID = Field(..., description="Pet's ID")
    clinic_id: UUID = Field(..., description="Clinic's ID")
    doctor_id: Optional[UUID] = Field(None, description="Assigned doctor's ID")
    owner_id: UUID = Field(..., description="Pet owner's ID")
    access_granted_at: datetime = Field(..., description="When access was granted")
    access_expires_at: datetime = Field(..., description="When access expires")
    status: str = Field(..., description="Current status")
    otp_id: Optional[UUID] = Field(None, description="OTP used for access")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    @field_serializer('id', 'pet_id', 'clinic_id', 'doctor_id', 'owner_id', 'otp_id')
    def serialize_uuid(self, value: Optional[UUID]) -> Optional[str]:
        """Serialize UUID to string for JSON response."""
        return str(value) if value else None
    
    model_config = ConfigDict(from_attributes=True)


class OTPGenerationResponse(BaseModel):
    """Schema for OTP generation response."""
    
    otp_id: str = Field(..., description="OTP ID")
    message: str = Field(..., description="Success message")
    expires_in_minutes: int = Field(..., description="Minutes until OTP expires")

