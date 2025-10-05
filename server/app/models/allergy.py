"""
Allergy model for the application.

This module defines the Allergy SQLAlchemy model representing
pet allergies and sensitivities.
"""

from datetime import datetime, date
from typing import Optional
import uuid
import enum

from sqlalchemy import Column, DateTime, Date, String, Text, Boolean, UUID, ForeignKey, JSON, Enum
from sqlalchemy.sql import func

from app.database import Base


class AllergyType(str, enum.Enum):
    """Allergy type enumeration."""
    FOOD = "food"
    MEDICATION = "medication"
    ENVIRONMENTAL = "environmental"
    FLEA = "flea"
    OTHER = "other"


class AllergySeverity(str, enum.Enum):
    """Allergy severity enumeration."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    LIFE_THREATENING = "life_threatening"


class Allergy(Base):
    """
    Allergy model representing pet allergies and sensitivities.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: ID of the pet with the allergy
        allergen: What the pet is allergic to
        allergy_type: Type of allergy
        severity: Severity of the allergy
        symptoms: Array of allergy symptoms (JSONB)
        reaction_description: Detailed description of reaction
        diagnosed_by_doctor_id: ID of the diagnosing doctor (optional)
        diagnosed_date: Date when allergy was diagnosed (optional)
        notes: Additional notes
        is_active: Whether allergy is currently relevant
        created_by_user_id: User who added this allergy
        created_at: Allergy record creation timestamp
        updated_at: Allergy record last update timestamp
    """
    
    __tablename__ = "allergies"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    allergen: str = Column(String(200), nullable=False)
    allergy_type: str = Column(
        Enum(AllergyType), 
        default=AllergyType.OTHER, 
        nullable=False,
        index=True
    )
    severity: str = Column(
        Enum(AllergySeverity), 
        default=AllergySeverity.MILD, 
        nullable=False,
        index=True
    )
    symptoms: dict = Column(JSON, nullable=False, default=dict)
    reaction_description: Optional[str] = Column(Text, nullable=True)
    diagnosed_by_doctor_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("doctor_profiles.id"), 
        nullable=True
    )
    diagnosed_date: Optional[date] = Column(Date, nullable=True)
    notes: Optional[str] = Column(Text, nullable=True)
    is_active: bool = Column(Boolean, default=True, nullable=False, index=True)
    created_by_user_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.public_id"), 
        nullable=False
    )
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
    
    def __repr__(self) -> str:
        """String representation of the Allergy model."""
        return f"<Allergy(id={self.id}, allergen='{self.allergen}', pet_id={self.pet_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": str(self.pet_id),
            "allergen": self.allergen,
            "allergy_type": self.allergy_type.value if self.allergy_type else None,
            "severity": self.severity.value if self.severity else None,
            "symptoms": self.symptoms,
            "reaction_description": self.reaction_description,
            "diagnosed_by_doctor_id": str(self.diagnosed_by_doctor_id) if self.diagnosed_by_doctor_id else None,
            "diagnosed_date": self.diagnosed_date.isoformat() if self.diagnosed_date else None,
            "notes": self.notes,
            "is_active": self.is_active,
            "created_by_user_id": str(self.created_by_user_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


