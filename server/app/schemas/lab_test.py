"""
Lab Test Pydantic schemas for request/response validation.

This module defines Pydantic models for lab test-related API operations.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, HttpUrl


class LabTestBase(BaseModel):
    """Base Lab Test schema with common fields."""
    
    test_name: str = Field(..., min_length=1, max_length=200, description="Name of test")
    test_type: str = Field(..., min_length=1, max_length=100, description="Type of test")
    ordered_at: datetime = Field(..., description="When test was ordered")
    performed_at: Optional[datetime] = Field(None, description="When test was performed")
    results: Optional[str] = Field(None, description="Test results as text")
    results_json: Optional[dict] = Field(default_factory=dict, description="Structured results")
    results_file_url: Optional[str] = Field(None, max_length=500, description="URL to results file")
    reference_ranges: Optional[dict] = Field(default_factory=dict, description="Normal value ranges")
    abnormal_flags: Optional[dict] = Field(default_factory=dict, description="Abnormal value flags")
    interpretation: Optional[str] = Field(None, description="Doctor's interpretation")
    is_abnormal: bool = Field(False, description="Whether results are abnormal")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "test_name": "Complete Blood Count (CBC)",
                "test_type": "Blood Work",
                "ordered_at": "2025-10-01T10:00:00",
                "performed_at": "2025-10-01T14:00:00",
                "results": "All values within normal range",
                "results_json": {
                    "wbc": 7.5,
                    "rbc": 5.2,
                    "hemoglobin": 14.5,
                    "hematocrit": 42
                },
                "reference_ranges": {
                    "wbc": "5.0-15.0",
                    "rbc": "5.0-8.5",
                    "hemoglobin": "12.0-18.0",
                    "hematocrit": "37-55"
                },
                "abnormal_flags": {},
                "interpretation": "Normal blood count. No concerns.",
                "is_abnormal": False
            }
        }
    )


class LabTestCreate(LabTestBase):
    """Schema for creating/ordering a new lab test."""
    
    pet_id: str = Field(..., description="Pet's ID")
    ordered_by_doctor_id: str = Field(..., description="Doctor who ordered the test")
    medical_record_id: Optional[str] = Field(None, description="Associated medical record ID")
    performed_by_clinic_id: Optional[str] = Field(None, description="Lab/clinic performing test")
    status: str = Field("ordered", description="Initial status")
    
    @field_validator('pet_id', 'ordered_by_doctor_id', 'medical_record_id', 'performed_by_clinic_id')
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
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Validate status."""
        valid_statuses = ['ordered', 'in_progress', 'completed', 'cancelled']
        if v.lower() not in valid_statuses:
            raise ValueError(f'status must be one of: {", ".join(valid_statuses)}')
        return v.lower()


class LabTestUpdate(BaseModel):
    """Schema for updating a lab test (e.g., adding results)."""
    
    performed_at: Optional[datetime] = None
    status: Optional[str] = None
    results: Optional[str] = None
    results_json: Optional[dict] = None
    results_file_url: Optional[str] = None
    abnormal_flags: Optional[dict] = None
    interpretation: Optional[str] = None
    is_abnormal: Optional[bool] = None
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Validate status."""
        if v is None:
            return v
        valid_statuses = ['ordered', 'in_progress', 'completed', 'cancelled']
        if v.lower() not in valid_statuses:
            raise ValueError(f'status must be one of: {", ".join(valid_statuses)}')
        return v.lower()


class LabTestResponse(LabTestBase):
    """Schema for lab test response."""
    
    id: str = Field(..., description="Lab test ID")
    medical_record_id: Optional[str] = Field(None, description="Associated medical record ID")
    pet_id: str = Field(..., description="Pet's ID")
    ordered_by_doctor_id: str = Field(..., description="Doctor who ordered")
    performed_by_clinic_id: Optional[str] = Field(None, description="Lab/clinic that performed test")
    status: str = Field(..., description="Current status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)

