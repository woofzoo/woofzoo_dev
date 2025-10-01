"""
Doctor-Clinic Association model for the application.

This module defines the DoctorClinicAssociation model for many-to-many 
relationships between doctors and clinics.
"""

from datetime import datetime
import uuid
import enum

from sqlalchemy import Column, DateTime, Boolean, UUID, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class EmploymentType(str, enum.Enum):
    """Employment type enumeration."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    VISITING = "visiting"
    CONTRACTOR = "contractor"


class DoctorClinicAssociation(Base):
    """
    Doctor-Clinic Association model for many-to-many relationship.
    
    Attributes:
        id: Primary key identifier (UUID)
        doctor_id: ID of the doctor profile
        clinic_id: ID of the clinic profile
        employment_type: Type of employment relationship
        is_active: Whether the association is currently active
        joined_at: When the association started
        created_at: Association creation timestamp
    """
    
    __tablename__ = "doctor_clinic_associations"
    __table_args__ = (
        UniqueConstraint('doctor_id', 'clinic_id', name='uq_doctor_clinic'),
    )
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("doctor_profiles.id"), 
        nullable=False,
        index=True
    )
    clinic_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("clinic_profiles.id"), 
        nullable=False,
        index=True
    )
    employment_type: str = Column(
        Enum(EmploymentType), 
        default=EmploymentType.FULL_TIME, 
        nullable=False
    )
    is_active: bool = Column(Boolean, default=True, nullable=False)
    joined_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    created_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the DoctorClinicAssociation model."""
        return f"<DoctorClinicAssociation(doctor_id={self.doctor_id}, clinic_id={self.clinic_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "doctor_id": str(self.doctor_id),
            "clinic_id": str(self.clinic_id),
            "employment_type": self.employment_type.value if self.employment_type else None,
            "is_active": self.is_active,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


