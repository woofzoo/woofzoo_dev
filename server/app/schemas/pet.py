"""
Pet Pydantic schemas for request/response validation.

This module defines Pydantic models for pet-related API operations.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict, validator

from app.data.pet_types import get_pet_types, get_breeds_for_type


class PetBase(BaseModel):
    """Base Pet schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=50, description="Pet's name")
    pet_type: str = Field(..., description="Pet type (DOG, CAT, BIRD, etc.)")
    breed: str = Field(..., description="Pet's breed")
    age: Optional[int] = Field(None, ge=0, le=30, description="Pet's age in years")
    gender: str = Field(default="Unknown", description="Pet's gender")
    weight: Optional[float] = Field(None, gt=0, description="Pet's weight")
    
    @validator('pet_type')
    def validate_pet_type(cls, v):
        """Validate pet type."""
        if v.upper() not in get_pet_types():
            raise ValueError(f"Invalid pet type. Must be one of: {', '.join(get_pet_types())}")
        return v.upper()
    
    @validator('breed')
    def validate_breed(cls, v, values):
        """Validate breed for the given pet type."""
        pet_type = values.get('pet_type')
        if pet_type and v not in get_breeds_for_type(pet_type):
            raise ValueError(f"Invalid breed '{v}' for pet type '{pet_type}'")
        return v
    
    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender."""
        valid_genders = ["Male", "Female", "Unknown"]
        if v not in valid_genders:
            raise ValueError(f"Invalid gender. Must be one of: {', '.join(valid_genders)}")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "age": 3,
                "gender": "Male",
                "weight": 25.5
            }
        }
    )


class PetCreate(PetBase):
    """Schema for creating a new pet."""
    pass


class PetUpdate(BaseModel):
    """Schema for updating an existing pet."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Pet's name")
    age: Optional[int] = Field(None, ge=0, le=30, description="Pet's age in years")
    gender: Optional[str] = Field(None, description="Pet's gender")
    weight: Optional[float] = Field(None, gt=0, description="Pet's weight")
    photos: Optional[Dict[str, Any]] = Field(None, description="Pet's photos")
    emergency_contacts: Optional[Dict[str, Any]] = Field(None, description="Emergency contact information")
    insurance_info: Optional[Dict[str, Any]] = Field(None, description="Insurance information")
    
    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender."""
        if v is not None:
            valid_genders = ["Male", "Female", "Unknown"]
            if v not in valid_genders:
                raise ValueError(f"Invalid gender. Must be one of: {', '.join(valid_genders)}")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Buddy",
                "age": 4,
                "gender": "Male",
                "weight": 26.0,
                "photos": {
                    "photo_1": {
                        "url": "https://example.com/photo1.jpg",
                        "caption": "Front view"
                    }
                },
                "emergency_contacts": {
                    "vet": {
                        "name": "Dr. Smith",
                        "phone": "+1234567890"
                    }
                },
                "insurance_info": {
                    "provider": "PetCare Insurance",
                    "policy_number": "PC123456"
                }
            }
        }
    )


class PetResponse(PetBase):
    """Schema for pet response."""
    
    id: str = Field(..., description="Pet unique identifier")
    pet_id: str = Field(..., description="Pet's unique ID (e.g., DOG-GOLDEN_RETRIEVER-000001)")
    owner_id: str = Field(..., description="Owner's ID")
    photos: Dict[str, Any] = Field(..., description="Pet's photos")
    emergency_contacts: Dict[str, Any] = Field(..., description="Emergency contact information")
    insurance_info: Dict[str, Any] = Field(..., description="Insurance information")
    is_active: bool = Field(..., description="Pet activation status")
    created_at: datetime = Field(..., description="Pet creation timestamp")
    updated_at: datetime = Field(..., description="Pet last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "pet_id": "DOG-GOLDEN_RETRIEVER-000001",
                "owner_id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Buddy",
                "pet_type": "DOG",
                "breed": "Golden Retriever",
                "age": 3,
                "gender": "Male",
                "weight": 25.5,
                "photos": {
                    "photo_1": {
                        "url": "https://example.com/photo1.jpg",
                        "caption": "Front view"
                    }
                },
                "emergency_contacts": {
                    "vet": {
                        "name": "Dr. Smith",
                        "phone": "+1234567890"
                    }
                },
                "insurance_info": {
                    "provider": "PetCare Insurance",
                    "policy_number": "PC123456"
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
                        "pet_id": "DOG-GOLDEN_RETRIEVER-000001",
                        "owner_id": "550e8400-e29b-41d4-a716-446655440001",
                        "name": "Buddy",
                        "pet_type": "DOG",
                        "breed": "Golden Retriever",
                        "age": 3,
                        "gender": "Male",
                        "weight": 25.5,
                        "photos": {},
                        "emergency_contacts": {},
                        "insurance_info": {},
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
    
    phone_number: str = Field(..., min_length=10, max_length=15, description="Owner's phone number")
    pet_name: str = Field(..., min_length=1, max_length=50, description="Pet's name")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone_number": "+1234567890",
                "pet_name": "Buddy"
            }
        }
    )
