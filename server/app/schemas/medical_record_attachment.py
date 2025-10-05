"""
Medical Record Attachment Pydantic schemas for request/response validation.

This module defines Pydantic models for medical record attachment-related API operations.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class MedicalRecordAttachmentBase(BaseModel):
    """Base Medical Record Attachment schema with common fields."""
    
    file_name: str = Field(..., min_length=1, max_length=255, description="Original filename")
    file_url: str = Field(..., min_length=1, max_length=500, description="Storage URL")
    file_type: str = Field(..., min_length=1, max_length=50, description="MIME type")
    file_size: int = Field(..., gt=0, description="Size in bytes")
    attachment_type: str = Field(..., description="Type of attachment")
    description: Optional[str] = Field(None, description="Description of attachment")
    
    @field_validator('attachment_type')
    @classmethod
    def validate_attachment_type(cls, v):
        """Validate attachment type."""
        valid_types = ['lab_result', 'xray', 'ultrasound', 'certificate', 'report', 'photo', 'other']
        if v.lower() not in valid_types:
            raise ValueError(f'attachment_type must be one of: {", ".join(valid_types)}')
        return v.lower()
    
    @field_validator('file_type')
    @classmethod
    def validate_file_type(cls, v):
        """Validate file type is a valid MIME type."""
        # Basic MIME type validation
        if '/' not in v:
            raise ValueError('file_type must be a valid MIME type (e.g., image/jpeg, application/pdf)')
        return v.lower()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "file_name": "bloodwork_results_2025-10-01.pdf",
                "file_url": "https://s3.amazonaws.com/bucket/files/bloodwork_results_2025-10-01.pdf",
                "file_type": "application/pdf",
                "file_size": 524288,
                "attachment_type": "lab_result",
                "description": "Complete blood count results from routine checkup"
            }
        }
    )


class MedicalRecordAttachmentCreate(MedicalRecordAttachmentBase):
    """Schema for creating a new medical record attachment."""
    
    pet_id: str = Field(..., description="Pet's ID")
    medical_record_id: Optional[str] = Field(None, description="Associated medical record ID")
    lab_test_id: Optional[str] = Field(None, description="Associated lab test ID")
    vaccination_id: Optional[str] = Field(None, description="Associated vaccination ID")
    
    @field_validator('pet_id', 'medical_record_id', 'lab_test_id', 'vaccination_id')
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
    
    @field_validator('medical_record_id', 'lab_test_id', 'vaccination_id')
    @classmethod
    def validate_at_least_one_reference(cls, v, info):
        """Ensure at least one reference is provided."""
        # This will be validated in the service layer
        return v


class MedicalRecordAttachmentUpdate(BaseModel):
    """Schema for updating a medical record attachment."""
    
    description: Optional[str] = None


class MedicalRecordAttachmentResponse(MedicalRecordAttachmentBase):
    """Schema for medical record attachment response."""
    
    id: str = Field(..., description="Attachment ID")
    medical_record_id: Optional[str] = Field(None, description="Associated medical record ID")
    lab_test_id: Optional[str] = Field(None, description="Associated lab test ID")
    vaccination_id: Optional[str] = Field(None, description="Associated vaccination ID")
    pet_id: str = Field(..., description="Pet's ID")
    uploaded_by_user_id: str = Field(..., description="User who uploaded")
    uploaded_by_role: str = Field(..., description="Role at upload time")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class FileUploadResponse(BaseModel):
    """Schema for file upload response."""
    
    file_url: str = Field(..., description="URL of uploaded file")
    file_name: str = Field(..., description="Name of uploaded file")
    file_size: int = Field(..., description="Size of uploaded file in bytes")

