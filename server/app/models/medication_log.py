"""
Medication Log model for the application.

This module defines the MedicationLog SQLAlchemy model representing
owner-managed medication tracking for pets.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, String, Text, UUID, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class MedicationLog(Base):
    """
    Medication Log model representing owner-managed medication tracking.
    
    This is separate from doctor prescriptions and allows owners to track
    when they administered medications to their pets.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: ID of the pet
        created_by_user_id: ID of the user who logged the medication
        medication_name: Name of the medication given
        dosage: Amount of medication given
        dosage_unit: Unit of dosage (e.g., "mg", "ml", "tablet")
        administered_at: Date and time when medication was given
        notes: Optional notes about the administration
        created_at: Log creation timestamp
        updated_at: Log last update timestamp
    """
    
    __tablename__ = "medication_logs"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    created_by_user_id: int = Column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    # Medication details
    medication_name: str = Column(String(200), nullable=False)
    dosage: str = Column(String(100), nullable=False)
    dosage_unit: str = Column(String(50), nullable=False)
    
    # Administration details
    administered_at: datetime = Column(DateTime, nullable=False, index=True)
    notes: Optional[str] = Column(Text, nullable=True)
    
    # Timestamps
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
        """String representation of the MedicationLog model."""
        return f"<MedicationLog(id={self.id}, medication='{self.medication_name}', pet_id={self.pet_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": str(self.pet_id),
            "created_by_user_id": self.created_by_user_id,
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "dosage_unit": self.dosage_unit,
            "administered_at": self.administered_at.isoformat() if self.administered_at else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

