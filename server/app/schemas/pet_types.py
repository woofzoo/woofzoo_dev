"""
Pet types and breeds Pydantic schemas.

This module defines Pydantic models for pet types and breeds API responses.
"""

from pydantic import BaseModel, Field, ConfigDict


class PetTypesResponse(BaseModel):
    """Schema for pet types response."""
    
    types: list[str] = Field(..., description="List of available pet types")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "types": ["DOG", "CAT", "BIRD", "FISH", "RABBIT", "HAMSTER", "GUINEA_PIG", "OTHER"]
            }
        }
    )


class PetBreedsResponse(BaseModel):
    """Schema for pet breeds response."""
    
    pet_type: str = Field(..., description="Pet type")
    breeds: list[str] = Field(..., description="List of breeds for the pet type")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_type": "DOG",
                "breeds": [
                    "Golden Retriever", "Labrador Retriever", "German Shepherd", "Bulldog",
                    "Beagle", "Poodle", "Rottweiler", "Yorkshire Terrier", "Boxer", "Dachshund",
                    "Chihuahua", "Great Dane", "Siberian Husky", "Border Collie", "Australian Shepherd",
                    "Pomeranian", "Shih Tzu", "Cavalier King Charles Spaniel", "Bernese Mountain Dog",
                    "Mixed Breed", "Other"
                ]
            }
        }
    )
