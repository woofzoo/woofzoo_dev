"""
Prescription Pydantic schemas for request/response validation.

This module defines Pydantic models for prescription-related API operations.
"""

from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer


class PrescriptionBase(BaseModel):
    """Base Prescription schema with common fields."""
    
    medication_name: str = Field(..., min_length=1, max_length=200, description="Name of medication")
    dosage: str = Field(..., min_length=1, max_length=100, description="Dosage amount (e.g., '10mg')")
    dosage_unit: str = Field(..., min_length=1, max_length=50, description="Unit of dosage (e.g., 'mg', 'ml')")
    frequency: str = Field(..., min_length=1, max_length=100, description="How often (e.g., 'Twice daily')")
    route: str = Field(..., min_length=1, max_length=50, description="Route (e.g., 'Oral', 'Topical')")
    duration: str = Field(..., min_length=1, max_length=100, description="Duration (e.g., '7 days')")
    instructions: Optional[str] = Field(None, description="Special administration instructions")
    prescribed_date: date = Field(..., description="Date prescribed")
    start_date: date = Field(..., description="Date to start medication")
    end_date: Optional[date] = Field(None, description="Date to stop medication")
    quantity: float = Field(..., gt=0, description="Amount prescribed")
    refills_allowed: int = Field(0, ge=0, description="Number of refills allowed")
    
    @field_validator('route')
    @classmethod
    def validate_route(cls, v):
        """Validate and normalize route."""
        valid_routes = ['oral', 'topical', 'injectable', 'intravenous', 'subcutaneous', 'intramuscular', 'other']
        v_lower = v.lower()
        if v_lower not in valid_routes:
            return v  # Allow custom routes but normalize known ones
        return v_lower.capitalize()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "medication_name": "Amoxicillin",
                "dosage": "250",
                "dosage_unit": "mg",
                "frequency": "Twice daily",
                "route": "Oral",
                "duration": "10 days",
                "instructions": "Give with food",
                "prescribed_date": "2025-10-01",
                "start_date": "2025-10-01",
                "end_date": "2025-10-11",
                "quantity": 20.0,
                "refills_allowed": 0
            }
        }
    )


class PrescriptionCreate(PrescriptionBase):
    """Schema for creating a new prescription."""
    
    medical_record_id: str = Field(..., description="Associated medical record ID")
    pet_id: str = Field(..., description="Pet's ID")
    prescribed_by_doctor_id: str = Field(..., description="Prescribing doctor's ID")
    
    @field_validator('medical_record_id', 'pet_id', 'prescribed_by_doctor_id')
    @classmethod
    def validate_uuid_fields(cls, v, info):
        """Validate UUID fields."""
        from uuid import UUID
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError(f'{info.field_name} must be a valid UUID')


class PrescriptionUpdate(BaseModel):
    """Schema for updating a prescription."""
    
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    instructions: Optional[str] = None


class PrescriptionResponse(PrescriptionBase):
    """Schema for prescription response."""
    
    id: UUID = Field(..., description="Prescription ID")
    medical_record_id: UUID = Field(..., description="Associated medical record ID")
    pet_id: UUID = Field(..., description="Pet's ID")
    prescribed_by_doctor_id: UUID = Field(..., description="Prescribing doctor's ID")
    is_active: bool = Field(..., description="Whether prescription is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    @field_serializer('id', 'medical_record_id', 'pet_id', 'prescribed_by_doctor_id')
    def serialize_uuid(self, value: UUID) -> str:
        """Serialize UUID to string for JSON response."""
        return str(value)
    
    model_config = ConfigDict(from_attributes=True)

