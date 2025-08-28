"""
Pet Pydantic schemas for request/response validation.

This module defines Pydantic models for pet-related API operations.
"""

from datetime import datetime
from typing import Optional, Any
import uuid

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.data.pet_types import validate_pet_type_and_breed


class PetBase(BaseModel):
    """Base Pet schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Pet's name")
    pet_type: str = Field(..., description="Type of pet (e.g., DOG, CAT)")
    breed: str = Field(..., description="Breed of the pet")
    age: Optional[int] = Field(None, ge=0, le=50, description="Pet's age in years")
    gender: Optional[str] = Field(None, description="Pet's gender (MALE, FEMALE)")
    weight: Optional[float] = Field(None, ge=0.1, le=500.0, description="Pet's weight in kg")
    photos: Optional[list[str]] = Field(None, description="List of photo URLs")
    emergency_contacts: Optional[dict[str, Any]] = Field(None, description="Emergency contact information")
    insurance_info: Optional[dict[str, Any]] = Field(None, description="Insurance information")
    
    @field_validator('pet_type', 'breed')
    @classmethod
    def validate_pet_type_and_breed(cls, v, info):
        """Validate pet type and breed combination."""
        if info.field_name == 'pet_type':
            return v.upper()
        elif info.field_name == 'breed':
            return v.title()
        return v
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        """Validate gender value."""
        if v is not None:
            v = v.upper()
            if v not in ['MALE', 'FEMALE']:
                raise ValueError('Gender must be either MALE or FEMALE')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "age": 3,
                "gender": "MALE",
                "weight": 25.5,
                "photos": ["https://example.com/photo1.jpg"],
                "emergency_contacts": {
                    "vet": {"name": "Dr. Smith", "phone": "+1234567890"},
                    "owner": {"name": "John Doe", "phone": "+1234567890"}
                },
                "insurance_info": {
                    "provider": "PetCare Insurance",
                    "policy_number": "PC123456789"
                }
            }
        }
    )


class PetCreate(PetBase):
    """Schema for creating a new pet."""
    
    owner_id: str = Field(..., description="Owner's unique identifier")
    
    @field_validator('owner_id')
    @classmethod
    def validate_owner_id(cls, v):
        """Convert UUID to string if needed."""
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "owner_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "age": 3,
                "gender": "MALE",
                "weight": 25.5,
                "photos": ["https://example.com/photo1.jpg"],
                "emergency_contacts": {
                    "vet": {"name": "Dr. Smith", "phone": "+1234567890"},
                    "owner": {"name": "John Doe", "phone": "+1234567890"}
                },
                "insurance_info": {
                    "provider": "PetCare Insurance",
                    "policy_number": "PC123456789"
                }
            }
        }
    )


class PetUpdate(BaseModel):
    """Schema for updating an existing pet."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Pet's name")
    pet_type: Optional[str] = Field(None, description="Type of pet (e.g., DOG, CAT)")
    breed: Optional[str] = Field(None, description="Breed of the pet")
    age: Optional[int] = Field(None, ge=0, le=50, description="Pet's age in years")
    gender: Optional[str] = Field(None, description="Pet's gender (MALE, FEMALE)")
    weight: Optional[float] = Field(None, ge=0.1, le=500.0, description="Pet's weight in kg")
    photos: Optional[list[str]] = Field(None, description="List of photo URLs")
    emergency_contacts: Optional[dict[str, Any]] = Field(None, description="Emergency contact information")
    insurance_info: Optional[dict[str, Any]] = Field(None, description="Insurance information")
    
    @field_validator('pet_type')
    @classmethod
    def validate_pet_type(cls, v):
        """Validate pet type."""
        if v is not None:
            return v.upper()
        return v
    
    @field_validator('breed')
    @classmethod
    def validate_breed(cls, v):
        """Validate breed."""
        if v is not None:
            return v.title()
        return v
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        """Validate gender value."""
        if v is not None:
            v = v.upper()
            if v not in ['MALE', 'FEMALE']:
                raise ValueError('Gender must be either MALE or FEMALE')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Buddy Jr.",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "age": 4,
                "gender": "MALE",
                "weight": 27.0,
                "photos": ["https://example.com/photo2.jpg"],
                "emergency_contacts": {
                    "vet": {"name": "Dr. Johnson", "phone": "+1234567890"},
                    "owner": {"name": "John Doe", "phone": "+1234567890"}
                },
                "insurance_info": {
                    "provider": "PetCare Insurance",
                    "policy_number": "PC123456789"
                }
            }
        }
    )


class PetResponse(PetBase):
    """Schema for pet response."""
    
    id: str = Field(..., description="Pet unique identifier")
    pet_id: str = Field(..., description="Pet's unique pet ID")
    owner_id: str = Field(..., description="Owner's unique identifier")
    is_active: bool = Field(..., description="Pet profile status")
    created_at: datetime = Field(..., description="Pet creation timestamp")
    updated_at: datetime = Field(..., description="Pet last update timestamp")
    
    @field_validator('id', 'owner_id', mode='before')
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
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "pet_id": "DOG-GOLDEN-RETRIEVER-000001",
                "owner_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "age": 3,
                "gender": "MALE",
                "weight": 25.5,
                "photos": ["https://example.com/photo1.jpg"],
                "emergency_contacts": {
                    "vet": {"name": "Dr. Smith", "phone": "+1234567890"},
                    "owner": {"name": "John Doe", "phone": "+1234567890"}
                },
                "insurance_info": {
                    "provider": "PetCare Insurance",
                    "policy_number": "PC123456789"
                },
                "is_active": True,
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:00:00Z"
            }
        }
    )


class PetListResponse(BaseModel):
    """Schema for list of pets response."""
    
    pets: list[PetResponse] = Field(..., description="List of pets")
    total: int = Field(..., description="Total number of pets")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pets": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "pet_id": "DOG-GOLDEN-RETRIEVER-000001",
                        "owner_id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Buddy",
                        "pet_type": "DOG",
                        "breed": "Golden Retriever",
                        "age": 3,
                        "gender": "MALE",
                        "weight": 25.5,
                        "photos": ["https://example.com/photo1.jpg"],
                        "emergency_contacts": {
                            "vet": {"name": "Dr. Smith", "phone": "+1234567890"},
                            "owner": {"name": "John Doe", "phone": "+1234567890"}
                        },
                        "insurance_info": {
                            "provider": "PetCare Insurance",
                            "policy_number": "PC123456789"
                        },
                        "is_active": True,
                        "created_at": "2025-01-01T12:00:00Z",
                        "updated_at": "2025-01-01T12:00:00Z"
                    }
                ],
                "total": 1
            }
        }
    )


class PetLookupRequest(BaseModel):
    """Schema for pet lookup request."""
    
    pet_id: str = Field(..., description="Pet's unique pet ID")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "DOG-GOLDEN-RETRIEVER-000001"
            }
        }
    )
