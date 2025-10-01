"""
Allergy Pydantic schemas for request/response validation.

This module defines Pydantic models for allergy-related API operations.
"""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class AllergyBase(BaseModel):
    """Base Allergy schema with common fields."""
    
    allergen: str = Field(..., min_length=1, max_length=200, description="What pet is allergic to")
    allergy_type: str = Field(..., description="Type of allergy")
    severity: str = Field(..., description="Severity level")
    symptoms: Optional[dict] = Field(default_factory=dict, description="Allergy symptoms")
    reaction_description: Optional[str] = Field(None, description="Detailed reaction description")
    diagnosed_date: Optional[date] = Field(None, description="Date diagnosed")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    @field_validator('allergy_type')
    @classmethod
    def validate_allergy_type(cls, v):
        """Validate allergy type."""
        valid_types = ['food', 'medication', 'environmental', 'flea', 'other']
        if v.lower() not in valid_types:
            raise ValueError(f'allergy_type must be one of: {", ".join(valid_types)}')
        return v.lower()
    
    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v):
        """Validate severity level."""
        valid_severities = ['mild', 'moderate', 'severe', 'life_threatening']
        if v.lower() not in valid_severities:
            raise ValueError(f'severity must be one of: {", ".join(valid_severities)}')
        return v.lower()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "allergen": "Chicken",
                "allergy_type": "food",
                "severity": "moderate",
                "symptoms": {
                    "itching": True,
                    "hives": True,
                    "vomiting": False,
                    "diarrhea": True
                },
                "reaction_description": "Develops skin rashes and digestive issues within 2-4 hours of consuming chicken",
                "diagnosed_date": "2024-06-15",
                "notes": "Switched to lamb-based diet with good results"
            }
        }
    )


class AllergyCreate(AllergyBase):
    """Schema for creating a new allergy record."""
    
    pet_id: str = Field(..., description="Pet's ID")
    diagnosed_by_doctor_id: Optional[str] = Field(None, description="Doctor who diagnosed")
    
    @field_validator('pet_id', 'diagnosed_by_doctor_id')
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


class AllergyUpdate(BaseModel):
    """Schema for updating an allergy record."""
    
    severity: Optional[str] = None
    symptoms: Optional[dict] = None
    reaction_description: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None
    
    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v):
        """Validate severity level."""
        if v is None:
            return v
        valid_severities = ['mild', 'moderate', 'severe', 'life_threatening']
        if v.lower() not in valid_severities:
            raise ValueError(f'severity must be one of: {", ".join(valid_severities)}')
        return v.lower()


class AllergyResponse(AllergyBase):
    """Schema for allergy response."""
    
    id: str = Field(..., description="Allergy ID")
    pet_id: str = Field(..., description="Pet's ID")
    diagnosed_by_doctor_id: Optional[str] = Field(None, description="Doctor who diagnosed")
    is_active: bool = Field(..., description="Whether allergy is currently relevant")
    created_by_user_id: str = Field(..., description="User who added this")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)

