"""
Prescription model for the application.

This module defines the Prescription SQLAlchemy model representing
medications prescribed to pets.
"""

from datetime import datetime, date
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, Date, String, Text, Float, Integer, Boolean, UUID, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Prescription(Base):
    """
    Prescription model representing medications prescribed to pets.
    
    Attributes:
        id: Primary key identifier (UUID)
        medical_record_id: ID of the associated medical visit
        pet_id: ID of the pet (denormalized for queries)
        medication_name: Name of the medication
        dosage: Dosage amount (e.g., "10mg")
        dosage_unit: Unit of dosage (e.g., "mg", "ml")
        frequency: How often to administer (e.g., "Twice daily")
        route: Route of administration (e.g., "Oral", "Topical")
        duration: Duration of treatment (e.g., "7 days")
        instructions: Special administration instructions
        prescribed_by_doctor_id: ID of the prescribing doctor
        prescribed_date: Date the prescription was written
        start_date: Date to start medication
        end_date: Date to end medication (if applicable)
        quantity: Amount prescribed
        refills_allowed: Number of refills allowed
        is_active: Whether prescription is currently active
        created_at: Prescription creation timestamp
        updated_at: Prescription last update timestamp
    """
    
    __tablename__ = "prescriptions"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medical_record_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("medical_records.id"), 
        nullable=False,
        index=True
    )
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    medication_name: str = Column(String(200), nullable=False)
    dosage: str = Column(String(100), nullable=False)
    dosage_unit: str = Column(String(50), nullable=False)
    frequency: str = Column(String(100), nullable=False)
    route: str = Column(String(50), nullable=False)
    duration: str = Column(String(100), nullable=False)
    instructions: Optional[str] = Column(Text, nullable=True)
    prescribed_by_doctor_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("doctor_profiles.id"), 
        nullable=False,
        index=True
    )
    prescribed_date: date = Column(Date, nullable=False)
    start_date: date = Column(Date, nullable=False)
    end_date: Optional[date] = Column(Date, nullable=True, index=True)
    quantity: float = Column(Float, nullable=False)
    refills_allowed: int = Column(Integer, default=0, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False, index=True)
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
        """String representation of the Prescription model."""
        return f"<Prescription(id={self.id}, medication='{self.medication_name}', pet_id={self.pet_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "medical_record_id": str(self.medical_record_id),
            "pet_id": str(self.pet_id),
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "dosage_unit": self.dosage_unit,
            "frequency": self.frequency,
            "route": self.route,
            "duration": self.duration,
            "instructions": self.instructions,
            "prescribed_by_doctor_id": str(self.prescribed_by_doctor_id),
            "prescribed_date": self.prescribed_date.isoformat() if self.prescribed_date else None,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "quantity": self.quantity,
            "refills_allowed": self.refills_allowed,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


