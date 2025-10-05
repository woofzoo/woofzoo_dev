"""
Doctor-Clinic Association Pydantic schemas for request/response validation.

This module defines Pydantic models for doctor-clinic association-related API operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer

from app.models.doctor_clinic_association import EmploymentType


class DoctorClinicAssociationBase(BaseModel):
    """Base Doctor-Clinic Association schema with common fields."""
    
    employment_type: EmploymentType = Field(
        default=EmploymentType.FULL_TIME,
        description="Type of employment relationship"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
                "clinic_id": "987fcdeb-51a2-43f1-9876-543210fedcba",
                "employment_type": "full_time"
            }
        }
    )


class DoctorClinicAssociationCreate(DoctorClinicAssociationBase):
    """Schema for creating a new doctor-clinic association."""
    
    doctor_id: str = Field(..., description="ID of the doctor profile")
    clinic_id: str = Field(..., description="ID of the clinic profile")
    
    @field_validator('doctor_id', 'clinic_id')
    @classmethod
    def validate_uuid(cls, v):
        """Validate ID is a valid UUID string."""
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError(f'{v} must be a valid UUID')


class DoctorClinicAssociationUpdate(BaseModel):
    """Schema for updating a doctor-clinic association."""
    
    employment_type: Optional[EmploymentType] = Field(None, description="Type of employment")
    is_active: Optional[bool] = Field(None, description="Whether association is active")


class DoctorClinicAssociationResponse(DoctorClinicAssociationBase):
    """Schema for doctor-clinic association response."""
    
    id: UUID = Field(..., description="Association ID")
    doctor_id: UUID = Field(..., description="ID of the doctor profile")
    clinic_id: UUID = Field(..., description="ID of the clinic profile")
    is_active: bool = Field(..., description="Whether association is active")
    joined_at: datetime = Field(..., description="When the association started")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    @field_serializer('id', 'doctor_id', 'clinic_id')
    def serialize_uuid(self, value: UUID) -> str:
        """Serialize UUID to string for JSON response."""
        return str(value)
    
    model_config = ConfigDict(from_attributes=True)

