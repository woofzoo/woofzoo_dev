"""
Family Member model for the application.

This module defines the FamilyMember SQLAlchemy model representing family members in the system.
"""

from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, String, Boolean, UUID, ForeignKey, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


class AccessLevel(str, enum.Enum):
    """Access level enumeration for family members."""
    FULL = "Full"
    READ_ONLY = "Read-Only"


class FamilyMember(Base):
    """
    Family Member model representing a family member in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        phone_number: Family member's phone number (unique identifier)
        name: Family member's full name
        family_id: ID of the family this member belongs to
        access_level: Access level (Full or Read-Only)
        is_active: Account activation status
        joined_at: When the member joined the family
        created_at: Family member creation timestamp
    """
    
    __tablename__ = "family_members"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # phone_number: str = Column(String(15), unique=True, nullable=False, index=True)
    # name: str = Column(String(100), nullable=False)
    family_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    access_level: str = Column(Enum(AccessLevel), default=AccessLevel.READ_ONLY, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.public_id"), nullable=False)
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
        """String representation of the FamilyMember model."""
        return f"<FamilyMember(id={self.id}, phone='{self.phone_number}', name='{self.name}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "phone_number": self.phone_number,
            "name": self.name,
            "family_id": str(self.family_id),
            "access_level": self.access_level.value if self.access_level else None,
            "is_active": self.is_active,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
