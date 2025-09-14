"""
Owner model for the application.

This module defines the Owner SQLAlchemy model representing pet owners in the system.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, String, Text, Boolean, UUID
from sqlalchemy.sql import func

from app.database import Base


class Owner(Base):
    """
    Owner model representing a pet owner in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        phone_number: Owner's phone number (unique identifier)
        name: Owner's full name
        email: Owner's email address (optional)
        address: Owner's address (optional)
        is_active: Account activation status
        created_at: Owner creation timestamp
        updated_at: Owner last update timestamp
    """
    
    __tablename__ = "owners"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number: str = Column(String(15), unique=True, nullable=False, index=True)
    name: str = Column(String(100), nullable=False)
    email: Optional[str] = Column(String(100), nullable=True)
    address: Optional[str] = Column(Text, nullable=True)
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
        """String representation of the Owner model."""
        return f"<Owner(id={self.id}, phone='{self.phone_number}', name='{self.name}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "phone_number": self.phone_number,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
