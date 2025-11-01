"""
Pet Journal Pydantic schemas for request/response validation.

This module defines Pydantic models for pet journal API operations.
"""

from datetime import datetime, date
from typing import Optional, Any
import uuid

from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field


# Valid entry types for journal entries
VALID_ENTRY_TYPES = [
    "daily_activity",
    "medication_given",
    "activity_event",
    "health_note"
]


class JournalDetails(BaseModel):
    """
    Structured details for journal entries.
    
    This provides a flexible but typed structure for additional
    journal entry information based on the entry type.
    """
    
    # Common fields across all entry types
    activity_duration_minute: Optional[int] = Field(None, description="Duration of activity in minutes")
    location: Optional[str] = Field(None, max_length=200, description="Location where activity occurred")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    # Medication-specific fields
    medication_name: Optional[str] = Field(None, max_length=200, description="Name of medication given")
    dosage: Optional[str] = Field(None, max_length=100, description="Dosage administered")
    time: Optional[str] = Field(None, max_length=50, description="Time medication was given")
    
    # Health-specific fields
    severity: Optional[str] = Field(None, max_length=50, description="Severity level (mild, moderate, severe)")
    symptoms: Optional[list[str]] = Field(None, description="List of observed symptoms")
    temperature: Optional[float] = Field(None, description="Body temperature if measured")
    
    # Activity-specific fields
    mood: Optional[str] = Field(None, max_length=50, description="Pet's mood during activity")
    activity_type: Optional[str] = Field(None, max_length=100, description="Type of activity")
    other_pets: Optional[list[str]] = Field(None, description="Other pets involved in activity")
    
    # Photos/media
    photo_urls: Optional[list[str]] = Field(None, description="URLs to related photos")
    
    # Allow additional fields for extensibility
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "example": {
                "activity_duration_minute": 30,
                "location": "Central Park",
                "mood": "happy",
                "notes": "Had a great time playing fetch"
            }
        }
    )



class PetJournalBase(BaseModel):
    """Base Pet Journal schema with common fields."""
    
    entry_type: str = Field(..., description="Type of journal entry (daily_activity, medication_given, activity_event, health_note)")
    title: str = Field(..., min_length=1, max_length=200, description="Brief title/summary of the entry")
    content: str = Field(..., min_length=1, description="Detailed content of the journal entry")
    entry_date: date = Field(..., description="Date the activity/event occurred")
    details: Optional[JournalDetails] = Field(default_factory=JournalDetails, description="Structured additional details")
    
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
                "details": {
                    "activity_duration_minute": 30,
                    "location": "Central Park",
                    "mood": "happy"
                }
            }
        }
    )


class PetJournalCreate(PetJournalBase):
    """Schema for creating a new pet journal entry."""
    
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
                "entry_type": "health_note",
                "title": "Slight cough observed",
                "content": "Noticed Buddy coughing a few times today. Will monitor for the next few days.",
                "entry_date": "2025-11-01",
                "details": {
                    "severity": "mild",
                    "symptoms": ["cough"],
                    "notes": "Will monitor for next few days"
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
    details: Optional[JournalDetails] = Field(None, description="Structured additional details")
    
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
                "content": "Updated content with more details",
                "details": {
                    "notes": "Additional observation noted"
                }
            }
        }
    )


class PetJournalResponse(BaseModel):
    """Schema for pet journal response."""
    
    id: str = Field(..., description="Journal entry unique identifier")
    pet_id: str = Field(..., description="Pet's unique identifier")
    created_by_user_id: int = Field(..., description="User who created the entry")
    entry_type: str = Field(..., description="Type of journal entry")
    title: str = Field(..., description="Brief title/summary of the entry")
    content: str = Field(..., description="Detailed content of the journal entry")
    entry_date: date = Field(..., description="Date the activity/event occurred")
    details: Optional[JournalDetails] = Field(default_factory=JournalDetails, validation_alias="details", serialization_alias="details", description="Structured additional details")
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
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "650e8400-e29b-41d4-a716-446655440001",
                "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_by_user_id": 1,
                "entry_type": "medication_given",
                "title": "Gave morning medication",
                "content": "Administered 10mg of medication as prescribed by vet.",
                "entry_date": "2025-11-01",
                "details": {
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
                        "details": {
                            "activity_duration_minute": 30,
                            "location": "Park"
                        },
                        "created_at": "2025-11-01T10:00:00Z",
                        "updated_at": "2025-11-01T10:00:00Z"
                    }
                ],
                "total": 1
            }
        }
    )

