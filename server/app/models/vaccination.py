"""
Vaccination model for the application.

This module defines the Vaccination SQLAlchemy model representing
pet vaccination history and schedules.
"""

from datetime import datetime, date
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, Date, String, Text, Boolean, UUID, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Vaccination(Base):
    """
    Vaccination model representing pet vaccination records.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: ID of the vaccinated pet
        medical_record_id: ID of the associated medical visit (optional)
        vaccine_name: Name of the vaccine (e.g., "Rabies", "DHPP")
        vaccine_type: Vaccine classification
        manufacturer: Vaccine manufacturer (optional)
        batch_number: Batch/lot number (optional)
        administered_by_doctor_id: ID of the administering doctor
        administered_at: When the vaccine was administered
        administration_site: Where vaccine was administered (e.g., "Left shoulder")
        clinic_id: ID of the clinic where administered
        next_due_date: When next dose is due
        is_booster: Whether this is a booster shot
        reaction_notes: Any adverse reactions (optional)
        certificate_url: URL to vaccination certificate (optional)
        is_required_by_law: Whether this is legally mandated
        created_at: Vaccination record creation timestamp
        updated_at: Vaccination record last update timestamp
    """
    
    __tablename__ = "vaccinations"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    medical_record_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("medical_records.id"), 
        nullable=True
    )
    vaccine_name: str = Column(String(200), nullable=False, index=True)
    vaccine_type: str = Column(String(100), nullable=False)
    manufacturer: Optional[str] = Column(String(200), nullable=True)
    batch_number: Optional[str] = Column(String(100), nullable=True)
    administered_by_doctor_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("doctor_profiles.id"), 
        nullable=False
    )
    administered_at: datetime = Column(DateTime, nullable=False, index=True)
    administration_site: Optional[str] = Column(String(100), nullable=True)
    clinic_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("clinic_profiles.id"), 
        nullable=False
    )
    next_due_date: Optional[date] = Column(Date, nullable=True, index=True)
    is_booster: bool = Column(Boolean, default=False, nullable=False)
    reaction_notes: Optional[str] = Column(Text, nullable=True)
    certificate_url: Optional[str] = Column(String(500), nullable=True)
    is_required_by_law: bool = Column(Boolean, default=False, nullable=False)
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
        """String representation of the Vaccination model."""
        return f"<Vaccination(id={self.id}, vaccine='{self.vaccine_name}', pet_id={self.pet_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": str(self.pet_id),
            "medical_record_id": str(self.medical_record_id) if self.medical_record_id else None,
            "vaccine_name": self.vaccine_name,
            "vaccine_type": self.vaccine_type,
            "manufacturer": self.manufacturer,
            "batch_number": self.batch_number,
            "administered_by_doctor_id": str(self.administered_by_doctor_id),
            "administered_at": self.administered_at.isoformat() if self.administered_at else None,
            "administration_site": self.administration_site,
            "clinic_id": str(self.clinic_id),
            "next_due_date": self.next_due_date.isoformat() if self.next_due_date else None,
            "is_booster": self.is_booster,
            "reaction_notes": self.reaction_notes,
            "certificate_url": self.certificate_url,
            "is_required_by_law": self.is_required_by_law,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


