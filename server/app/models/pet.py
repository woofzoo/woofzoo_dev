"""
Pet model for the application.

This module defines the Pet SQLAlchemy model representing pets in the system.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, String, Integer, Float, Boolean, UUID, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base
from app.data.pet_types import validate_pet_type_and_breed


class Gender(str, enum.Enum):
    """Gender enumeration for pets."""
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"


class Pet(Base):
    """
    Pet model representing a pet in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: Unique pet identifier (e.g., DOG-GOLDEN_RETRIEVER-000001)
        owner_id: ID of the pet owner
        name: Pet's name
        pet_type: Type of pet (DOG, CAT, BIRD, etc.)
        breed: Pet's breed
        age: Pet's age in years (optional)
        gender: Pet's gender (Male, Female, Unknown)
        weight: Pet's weight (optional)
        photos: JSON object containing photo URLs and metadata
        emergency_contacts: JSON object containing emergency contact information
        insurance_info: JSON object containing insurance information
        is_active: Pet activation status
        created_at: Pet creation timestamp
        updated_at: Pet last update timestamp
    """
    
    __tablename__ = "pets"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: str = Column(String(50), unique=True, nullable=False, index=True)
    owner_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)
    name: str = Column(String(50), nullable=False)
    pet_type: str = Column(String(20), nullable=False)
    breed: str = Column(String(50), nullable=False)
    age: Optional[int] = Column(Integer, nullable=True)
    gender: str = Column(Enum(Gender), default=Gender.UNKNOWN, nullable=False)
    weight: Optional[float] = Column(Float, nullable=True)
    photos: dict = Column(JSON, nullable=False, default=dict)
    emergency_contacts: dict = Column(JSON, nullable=False, default=dict)
    insurance_info: dict = Column(JSON, nullable=False, default=dict)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    def __init__(self, **kwargs):
        """Initialize pet with validation."""
        # Validate pet type and breed before creating
        pet_type = kwargs.get('pet_type')
        breed = kwargs.get('breed')
        if pet_type and breed:
            if not validate_pet_type_and_breed(pet_type, breed):
                raise ValueError(f"Invalid pet type '{pet_type}' or breed '{breed}'")
        super().__init__(**kwargs)
    
    def __repr__(self) -> str:
        """String representation of the Pet model."""
        return f"<Pet(id={self.id}, pet_id='{self.pet_id}', name='{self.name}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": self.pet_id,
            "owner_id": str(self.owner_id),
            "name": self.name,
            "pet_type": self.pet_type,
            "breed": self.breed,
            "age": self.age,
            "gender": self.gender.value if self.gender else None,
            "weight": self.weight,
            "photos": self.photos,
            "emergency_contacts": self.emergency_contacts,
            "insurance_info": self.insurance_info,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
