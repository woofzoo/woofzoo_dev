"""
Medical Record Pydantic schemas for request/response validation.

This module defines Pydantic models for medical record-related API operations.
"""

from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer


class MedicalRecordBase(BaseModel):
    """Base Medical Record schema with common fields."""
    
    visit_date: datetime = Field(..., description="Date and time of visit")
    visit_type: str = Field(..., description="Type of visit")
    chief_complaint: Optional[str] = Field(None, description="Presenting problem")
    diagnosis: Optional[str] = Field(None, description="Doctor's diagnosis")
    symptoms: Optional[dict] = Field(default_factory=dict, description="Observed symptoms")
    treatment_plan: Optional[str] = Field(None, description="Recommended treatment")
    clinical_notes: Optional[str] = Field(None, description="Detailed doctor notes")
    weight: Optional[float] = Field(None, ge=0.1, le=500.0, description="Pet weight in kg")
    temperature: Optional[float] = Field(None, ge=30.0, le=45.0, description="Body temperature in °C")
    vital_signs: Optional[dict] = Field(default_factory=dict, description="Heart rate, respiratory rate, etc.")
    follow_up_required: bool = Field(False, description="Whether follow-up is needed")
    follow_up_date: Optional[date] = Field(None, description="Recommended follow-up date")
    follow_up_notes: Optional[str] = Field(None, description="Follow-up instructions")
    is_emergency: bool = Field(False, description="Was this an emergency visit")
    
    @field_validator('visit_type')
    @classmethod
    def validate_visit_type(cls, v):
        """Validate visit type."""
        valid_types = ['routine_checkup', 'emergency', 'surgery', 'vaccination', 'follow_up', 'other']
        if v.lower() not in valid_types:
            raise ValueError(f'visit_type must be one of: {", ".join(valid_types)}')
        return v.lower()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "visit_date": "2025-10-01T10:30:00",
                "visit_type": "routine_checkup",
                "chief_complaint": "Annual wellness check",
                "diagnosis": "Healthy, no issues found",
                "symptoms": {"lethargy": False, "appetite_loss": False},
                "treatment_plan": "Continue current diet and exercise",
                "clinical_notes": "Pet is in excellent health. All vital signs normal.",
                "weight": 25.5,
                "temperature": 38.5,
                "vital_signs": {"heart_rate": 80, "respiratory_rate": 20},
                "follow_up_required": True,
                "follow_up_date": "2026-10-01",
                "follow_up_notes": "Schedule annual checkup",
                "is_emergency": False
            }
        }
    )


class MedicalRecordCreate(MedicalRecordBase):
    """Schema for creating a new medical record."""
    
    pet_id: str = Field(..., description="Pet's ID")
    clinic_id: str = Field(..., description="Clinic's ID")
    doctor_id: str = Field(..., description="Doctor's ID")
    
    @field_validator('pet_id', 'clinic_id', 'doctor_id')
    @classmethod
    def validate_uuid_fields(cls, v, info):
        """Validate UUID fields."""
        from uuid import UUID
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError(f'{info.field_name} must be a valid UUID')


class MedicalRecordUpdate(BaseModel):
    """Schema for updating a medical record (admin corrections only)."""
    
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    clinical_notes: Optional[str] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[date] = None
    follow_up_notes: Optional[str] = None


class MedicalRecordResponse(MedicalRecordBase):
    """Schema for medical record response."""
    
    id: UUID = Field(..., description="Medical record ID")
    pet_id: UUID = Field(..., description="Pet's ID")
    clinic_id: UUID = Field(..., description="Clinic's ID")
    doctor_id: UUID = Field(..., description="Doctor's ID")
    created_by_user_id: UUID = Field(..., description="User who created the record")
    created_by_role: str = Field(..., description="Role at time of creation")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    @field_serializer('id', 'pet_id', 'clinic_id', 'doctor_id', 'created_by_user_id')
    def serialize_uuid(self, value: UUID) -> str:
        """Serialize UUID to string for JSON response."""
        return str(value)
    
    model_config = ConfigDict(from_attributes=True)


class MedicalRecordListResponse(BaseModel):
    """Schema for list of medical records with pagination."""
    
    records: list[MedicalRecordResponse] = Field(..., description="List of medical records")
    total: int = Field(..., description="Total number of records")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum records returned")

