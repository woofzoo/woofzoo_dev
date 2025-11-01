"""
Pet Journal Pydantic schemas for request/response validation.

This module defines Pydantic models for pet journal API operations.
"""

from datetime import datetime, date
from typing import Optional, Any
import uuid

from pydantic import BaseModel, Field, ConfigDict, field_validator


# Valid entry types for journal entries
VALID_ENTRY_TYPES = [
    "daily_activity",
    "medication_given",
    "activity_event",
    "health_note"
]


class PetJournalBase(BaseModel):
    """Base Pet Journal schema with common fields."""
    
    entry_type: str = Field(..., description="Type of journal entry (daily_activity, medication_given, activity_event, health_note)")
    title: str = Field(..., min_length=1, max_length=200, description="Brief title/summary of the entry")
    content: str = Field(..., min_length=1, description="Detailed content of the journal entry")
    entry_date: date = Field(..., description="Date the activity/event occurred")
    metadata: Optional[dict[str, Any]] = Field(default_factory=dict, description="Additional flexible metadata")
    
    @field_validator('entry_type')
    @classmethod
    def validate_entry_type(cls, v):
        """Validate entry type is one of the allowed values."""
        if v not in VALID_ENTRY_TYPES:
            raise ValueError(f"Entry type must be one of: {', '.join(VALID_ENTRY_TYPES)}")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "entry_type": "daily_activity",
                "title": "Morning walk at the park",
                "content": "Buddy had a great time at the park this morning. He played fetch for 30 minutes and socialized with other dogs.",
                "entry_date": "2025-11-01",
                "metadata": {
                    "duration_minutes": 30,
                    "location": "Central Park",
                    "mood": "happy"
                }
            }
        }
    )


class PetJournalCreate(PetJournalBase):
    """Schema for creating a new pet journal entry."""
    
    pet_id: str = Field(..., description="Pet's unique identifier")
    
    @field_validator('pet_id')
    @classmethod
    def validate_pet_id(cls, v):
        """Convert UUID to string if needed."""
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                "entry_type": "health_note",
                "title": "Slight cough observed",
                "content": "Noticed Buddy coughing a few times today. Will monitor for the next few days.",
                "entry_date": "2025-11-01",
                "metadata": {
                    "severity": "mild",
                    "frequency": "occasional"
                }
            }
        }
    )


class PetJournalUpdate(BaseModel):
    """Schema for updating an existing pet journal entry."""
    
    entry_type: Optional[str] = Field(None, description="Type of journal entry")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Brief title/summary")
    content: Optional[str] = Field(None, min_length=1, description="Detailed content")
    entry_date: Optional[date] = Field(None, description="Date the activity/event occurred")
    metadata: Optional[dict[str, Any]] = Field(None, description="Additional flexible metadata")
    
    @field_validator('entry_type')
    @classmethod
    def validate_entry_type(cls, v):
        """Validate entry type is one of the allowed values."""
        if v is not None and v not in VALID_ENTRY_TYPES:
            raise ValueError(f"Entry type must be one of: {', '.join(VALID_ENTRY_TYPES)}")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated title",
                "content": "Updated content with more details"
            }
        }
    )


class PetJournalResponse(PetJournalBase):
    """Schema for pet journal response."""
    
    id: str = Field(..., description="Journal entry unique identifier")
    pet_id: str = Field(..., description="Pet's unique identifier")
    created_by_user_id: int = Field(..., description="User who created the entry")
    created_at: datetime = Field(..., description="Entry creation timestamp")
    updated_at: datetime = Field(..., description="Entry last update timestamp")
    
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
                "id": "650e8400-e29b-41d4-a716-446655440001",
                "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_by_user_id": 1,
                "entry_type": "medication_given",
                "title": "Gave morning medication",
                "content": "Administered 10mg of medication as prescribed by vet.",
                "entry_date": "2025-11-01",
                "metadata": {
                    "medication_name": "Antibiotics",
                    "dosage": "10mg",
                    "time": "08:00 AM"
                },
                "created_at": "2025-11-01T08:30:00Z",
                "updated_at": "2025-11-01T08:30:00Z"
            }
        }
    )


class PetJournalListResponse(BaseModel):
    """Schema for list of pet journal entries response."""
    
    entries: list[PetJournalResponse] = Field(..., description="List of journal entries")
    total: int = Field(..., description="Total number of entries")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "entries": [
                    {
                        "id": "650e8400-e29b-41d4-a716-446655440001",
                        "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                        "created_by_user_id": 1,
                        "entry_type": "daily_activity",
                        "title": "Morning walk",
                        "content": "30 minute walk in the park",
                        "entry_date": "2025-11-01",
                        "metadata": {},
                        "created_at": "2025-11-01T10:00:00Z",
                        "updated_at": "2025-11-01T10:00:00Z"
                    }
                ],
                "total": 1
            }
        }
    )

