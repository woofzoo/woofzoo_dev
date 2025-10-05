"""
Doctor Profile model for the application.

This module defines the DoctorProfile SQLAlchemy model representing veterinarian information.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, String, Text, Integer, Boolean, UUID, ForeignKey, JSON
from sqlalchemy.sql import func

from app.database import Base


class DoctorProfile(Base):
    """
    Doctor Profile model representing a veterinarian in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        user_id: ID of the user account for this doctor
        license_number: Veterinary license number
        specialization: Doctor's specialization (e.g., Surgery, Dentistry)
        years_of_experience: Years of practicing experience
        qualifications: Array of degrees and certifications (JSONB)
        bio: Professional biography
        is_verified: Whether the license is verified
        is_active: Whether the doctor is currently practicing
        created_at: Doctor profile creation timestamp
        updated_at: Doctor profile last update timestamp
    """
    
    __tablename__ = "doctor_profiles"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.public_id"), 
        nullable=False, 
        unique=True,
        index=True
    )
    license_number: str = Column(String(100), nullable=False, unique=True, index=True)
    specialization: Optional[str] = Column(String(100), nullable=True, index=True)
    years_of_experience: Optional[int] = Column(Integer, nullable=True)
    qualifications: dict = Column(JSON, nullable=False, default=dict)
    bio: Optional[str] = Column(Text, nullable=True)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
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
    
    def __repr__(self) -> str:
        """String representation of the DoctorProfile model."""
        return f"<DoctorProfile(id={self.id}, license='{self.license_number}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "license_number": self.license_number,
            "specialization": self.specialization,
            "years_of_experience": self.years_of_experience,
            "qualifications": self.qualifications,
            "bio": self.bio,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


