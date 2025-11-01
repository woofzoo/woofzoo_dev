"""
Medication Log Pydantic schemas for request/response validation.

This module defines Pydantic models for medication log API operations.
"""

from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field, ConfigDict, field_validator


class MedicationLogBase(BaseModel):
    """Base Medication Log schema with common fields."""
    
    medication_name: str = Field(..., min_length=1, max_length=200, description="Name of the medication")
    dosage: str = Field(..., min_length=1, max_length=100, description="Amount of medication given")
    dosage_unit: str = Field(..., min_length=1, max_length=50, description="Unit of dosage (e.g., mg, ml, tablet)")
    administered_at: datetime = Field(..., description="Date and time when medication was given")
    notes: Optional[str] = Field(None, description="Optional notes about the administration")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "medication_name": "Amoxicillin",
                "dosage": "250",
                "dosage_unit": "mg",
                "administered_at": "2025-11-01T08:00:00Z",
                "notes": "Given with breakfast. Pet took it well."
            }
        }
    )


class MedicationLogCreate(MedicationLogBase):
    """Schema for creating a new medication log entry."""
    
    pet_id: Optional[str] = Field(None, description="Pet's unique identifier (auto-filled from URL)")
    
    @field_validator('pet_id')
    @classmethod
    def validate_pet_id(cls, v):
        """Convert UUID to string if needed."""
        if v is None:
            return None
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "medication_name": "Amoxicillin",
                "dosage": "250",
                "dosage_unit": "mg",
                "administered_at": "2025-11-01T08:00:00Z",
                "notes": "Given with breakfast"
            }
        }
    )


class MedicationLogUpdate(BaseModel):
    """Schema for updating an existing medication log entry."""
    
    medication_name: Optional[str] = Field(None, min_length=1, max_length=200, description="Name of the medication")
    dosage: Optional[str] = Field(None, min_length=1, max_length=100, description="Amount of medication given")
    dosage_unit: Optional[str] = Field(None, min_length=1, max_length=50, description="Unit of dosage")
    administered_at: Optional[datetime] = Field(None, description="Date and time when medication was given")
    notes: Optional[str] = Field(None, description="Optional notes about the administration")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notes": "Updated notes: Pet showed good response to medication"
            }
        }
    )


class MedicationLogResponse(MedicationLogBase):
    """Schema for medication log response."""
    
    id: str = Field(..., description="Medication log unique identifier")
    pet_id: str = Field(..., description="Pet's unique identifier")
    created_by_user_id: int = Field(..., description="User who logged the medication")
    created_at: datetime = Field(..., description="Log creation timestamp")
    updated_at: datetime = Field(..., description="Log last update timestamp")
    
    @field_validator('id', 'pet_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        """Convert UUID objects to strings."""
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "750e8400-e29b-41d4-a716-446655440002",
                "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_by_user_id": 1,
                "medication_name": "Amoxicillin",
                "dosage": "250",
                "dosage_unit": "mg",
                "administered_at": "2025-11-01T08:00:00Z",
                "notes": "Given with breakfast. Pet took it well.",
                "created_at": "2025-11-01T08:05:00Z",
                "updated_at": "2025-11-01T08:05:00Z"
            }
        }
    )


class MedicationLogListResponse(BaseModel):
    """Schema for list of medication logs response."""
    
    logs: list[MedicationLogResponse] = Field(..., description="List of medication logs")
    total: int = Field(..., description="Total number of logs")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "logs": [
                    {
                        "id": "750e8400-e29b-41d4-a716-446655440002",
                        "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                        "created_by_user_id": 1,
                        "medication_name": "Amoxicillin",
                        "dosage": "250",
                        "dosage_unit": "mg",
                        "administered_at": "2025-11-01T08:00:00Z",
                        "notes": "Given with breakfast",
                        "created_at": "2025-11-01T08:05:00Z",
                        "updated_at": "2025-11-01T08:05:00Z"
                    }
                ],
                "total": 1
            }
        }
    )

