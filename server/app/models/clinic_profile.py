"""
Clinic Profile model for the application.

This module defines the ClinicProfile SQLAlchemy model representing clinic information.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, String, Text, Boolean, UUID, ForeignKey, JSON
from sqlalchemy.sql import func

from app.database import Base


class ClinicProfile(Base):
    """
    Clinic Profile model representing a veterinary clinic in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        user_id: ID of the user who owns/administers this clinic
        clinic_name: Official name of the clinic
        license_number: Business license number
        address: Full clinic address
        phone: Clinic contact phone number
        email: Clinic contact email
        operating_hours: Operating schedule (JSONB)
        services_offered: List of services provided (JSONB)
        is_verified: Whether the clinic is verified
        is_active: Whether the clinic is currently active
        created_at: Clinic profile creation timestamp
        updated_at: Clinic profile last update timestamp
    """
    
    __tablename__ = "clinic_profiles"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.public_id"), 
        nullable=False, 
        unique=True,
        index=True
    )
    clinic_name: str = Column(String(200), nullable=False, index=True)
    license_number: str = Column(String(100), nullable=False, unique=True, index=True)
    address: str = Column(Text, nullable=False)
    phone: str = Column(String(20), nullable=False)
    email: str = Column(String(255), nullable=False)
    operating_hours: dict = Column(JSON, nullable=False, default=dict)
    services_offered: dict = Column(JSON, nullable=False, default=dict)
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
        """String representation of the ClinicProfile model."""
        return f"<ClinicProfile(id={self.id}, name='{self.clinic_name}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "clinic_name": self.clinic_name,
            "license_number": self.license_number,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "operating_hours": self.operating_hours,
            "services_offered": self.services_offered,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


