"""
Pet Clinic Access model for the application.

This module defines the PetClinicAccess model for managing OTP-based
access control for clinic visits.
"""

from datetime import datetime
from typing import Optional
import uuid
import enum

from sqlalchemy import Column, DateTime, String, UUID, ForeignKey, Enum, Index
from sqlalchemy.sql import func

from app.database import Base


class AccessStatus(str, enum.Enum):
    """Access status enumeration."""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class PetClinicAccess(Base):
    """
    Pet Clinic Access model for managing clinic access to pet records.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: ID of the pet being accessed
        clinic_id: ID of the clinic accessing the pet
        doctor_id: ID of the assigned doctor (optional)
        owner_id: ID of the pet owner who granted access
        access_granted_at: When OTP was validated and access granted
        access_expires_at: When the access expires
        status: Current status of the access
        otp_id: Reference to the OTP used (optional)
        purpose: Reason for the visit
        created_at: Access record creation timestamp
    """
    
    __tablename__ = "pet_clinic_access"
    __table_args__ = (
        Index('idx_pet_clinic_status', 'pet_id', 'clinic_id', 'status'),
    )
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    clinic_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("clinic_profiles.id"), 
        nullable=False,
        index=True
    )
    doctor_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("doctor_profiles.id"), 
        nullable=True,
        index=True
    )
    owner_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.public_id"), 
        nullable=False
    )
    access_granted_at: datetime = Column(DateTime, nullable=False)
    access_expires_at: datetime = Column(DateTime, nullable=False, index=True)
    status: str = Column(
        Enum(AccessStatus), 
        default=AccessStatus.ACTIVE, 
        nullable=False,
        index=True
    )
    otp_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("otps.id"), 
        nullable=True
    )
    purpose: Optional[str] = Column(String(200), nullable=True)
    created_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the PetClinicAccess model."""
        return f"<PetClinicAccess(pet_id={self.pet_id}, clinic_id={self.clinic_id}, status={self.status})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": str(self.pet_id),
            "clinic_id": str(self.clinic_id),
            "doctor_id": str(self.doctor_id) if self.doctor_id else None,
            "owner_id": str(self.owner_id),
            "access_granted_at": self.access_granted_at.isoformat() if self.access_granted_at else None,
            "access_expires_at": self.access_expires_at.isoformat() if self.access_expires_at else None,
            "status": self.status.value if self.status else None,
            "otp_id": str(self.otp_id) if self.otp_id else None,
            "purpose": self.purpose,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

