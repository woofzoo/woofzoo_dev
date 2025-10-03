"""
Doctor Profile Pydantic schemas for request/response validation.

This module defines Pydantic models for doctor profile-related API operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer


class DoctorProfileBase(BaseModel):
    """Base Doctor Profile schema with common fields."""
    
    license_number: str = Field(..., min_length=1, max_length=100, description="Veterinary license number")
    specialization: Optional[str] = Field(None, max_length=100, description="Doctor's specialization")
    years_of_experience: Optional[int] = Field(None, ge=0, le=70, description="Years of experience")
    qualifications: Optional[dict] = Field(default_factory=dict, description="Degrees and certifications")
    bio: Optional[str] = Field(None, max_length=2000, description="Professional biography")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "license_number": "DVM-2018-45678",
                "specialization": "Surgery",
                "years_of_experience": 8,
                "qualifications": {
                    "degree": "Doctor of Veterinary Medicine",
                    "university": "University of Illinois",
                    "year": 2015,
                    "certifications": ["Board Certified Surgeon", "Emergency Medicine"]
                },
                "bio": "Dr. Jane Smith is a board-certified veterinary surgeon with over 8 years of experience..."
            }
        }
    )


class DoctorProfileCreate(DoctorProfileBase):
    """Schema for creating a new doctor profile."""
    
    user_id: str = Field(..., description="User ID of the doctor")
    
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


class DoctorProfileUpdate(BaseModel):
    """Schema for updating a doctor profile."""
    
    specialization: Optional[str] = Field(None, max_length=100)
    years_of_experience: Optional[int] = Field(None, ge=0, le=70)
    qualifications: Optional[dict] = None
    bio: Optional[str] = Field(None, max_length=2000)
    is_active: Optional[bool] = None


class DoctorProfileResponse(DoctorProfileBase):
    """Schema for doctor profile response."""
    
    id: UUID = Field(..., description="Doctor profile ID")
    user_id: UUID = Field(..., description="User ID of the doctor")
    is_verified: bool = Field(..., description="Whether license is verified")
    is_active: bool = Field(..., description="Whether doctor is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    @field_serializer('id', 'user_id')
    def serialize_uuid(self, value: UUID) -> str:
        """Serialize UUID to string for JSON response."""
        return str(value)
    
    model_config = ConfigDict(from_attributes=True)

