"""
Vaccination Pydantic schemas for request/response validation.

This module defines Pydantic models for vaccination-related API operations.
"""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class VaccinationBase(BaseModel):
    """Base Vaccination schema with common fields."""
    
    vaccine_name: str = Field(..., min_length=1, max_length=200, description="Name of vaccine")
    vaccine_type: str = Field(..., min_length=1, max_length=100, description="Vaccine classification")
    manufacturer: Optional[str] = Field(None, max_length=200, description="Vaccine manufacturer")
    batch_number: Optional[str] = Field(None, max_length=100, description="Batch/lot number")
    administered_at: datetime = Field(..., description="When vaccine was administered")
    administration_site: Optional[str] = Field(None, max_length=100, description="Where administered")
    next_due_date: Optional[date] = Field(None, description="When next dose is due")
    is_booster: bool = Field(False, description="Is this a booster shot")
    reaction_notes: Optional[str] = Field(None, description="Any adverse reactions")
    certificate_url: Optional[str] = Field(None, max_length=500, description="Vaccination certificate URL")
    is_required_by_law: bool = Field(False, description="Legally mandated vaccine")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vaccine_name": "Rabies",
                "vaccine_type": "Core Vaccine",
                "manufacturer": "Zoetis",
                "batch_number": "LOT123456",
                "administered_at": "2025-10-01T10:30:00",
                "administration_site": "Left shoulder",
                "next_due_date": "2028-10-01",
                "is_booster": False,
                "reaction_notes": None,
                "certificate_url": "https://example.com/cert/rabies-2025.pdf",
                "is_required_by_law": True
            }
        }
    )


class VaccinationCreate(VaccinationBase):
    """Schema for creating a new vaccination record."""
    
    pet_id: str = Field(..., description="Pet's ID")
    administered_by_doctor_id: str = Field(..., description="Doctor who administered")
    clinic_id: str = Field(..., description="Clinic where administered")
    medical_record_id: Optional[str] = Field(None, description="Associated medical record ID")
    
    @field_validator('pet_id', 'administered_by_doctor_id', 'clinic_id', 'medical_record_id')
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


class VaccinationUpdate(BaseModel):
    """Schema for updating a vaccination record."""
    
    next_due_date: Optional[date] = None
    reaction_notes: Optional[str] = None
    certificate_url: Optional[str] = None


class VaccinationResponse(VaccinationBase):
    """Schema for vaccination response."""
    
    id: str = Field(..., description="Vaccination ID")
    pet_id: str = Field(..., description="Pet's ID")
    medical_record_id: Optional[str] = Field(None, description="Associated medical record ID")
    administered_by_doctor_id: str = Field(..., description="Doctor who administered")
    clinic_id: str = Field(..., description="Clinic where administered")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class VaccinationDueResponse(BaseModel):
    """Schema for vaccination due notification."""
    
    vaccination: VaccinationResponse
    days_until_due: int = Field(..., description="Days until next dose is due")
    is_overdue: bool = Field(..., description="Whether vaccine is overdue")

