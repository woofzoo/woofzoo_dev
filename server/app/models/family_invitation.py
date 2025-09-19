"""
Family Invitation model for the application.

This module defines the FamilyInvitation SQLAlchemy model for managing
family invitations with expiry dates.
"""

from datetime import datetime, timezone
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, String, Boolean, UUID, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class FamilyInvitation(Base):
    """
    Family Invitation model representing a family invitation in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        family_id: ID of the family being invited to
        invited_phone: Phone number of the invited person
        invited_name: Name of the invited person
        invited_by: ID of the owner who sent the invitation
        invite_code: Unique invitation code
        expires_at: When the invitation expires
        is_accepted: Whether the invitation has been accepted
        accepted_at: When the invitation was accepted
        created_at: Invitation creation timestamp
    """
    
    __tablename__ = "family_invitations"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    invited_phone: str = Column(String(15), nullable=False, index=True)
    invited_name: str = Column(String(100), nullable=False)
    invited_by: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)
    invite_code: str = Column(String(10), unique=True, nullable=False, index=True)
    expires_at: datetime = Column(DateTime, nullable=False)
    is_accepted: bool = Column(Boolean, default=False, nullable=False)
    accepted_at: Optional[datetime] = Column(DateTime, nullable=True)
    created_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the FamilyInvitation model."""
        return f"<FamilyInvitation(id={self.id}, invited_phone='{self.invited_phone}', invite_code='{self.invite_code}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "family_id": str(self.family_id),
            "invited_phone": self.invited_phone,
            "invited_name": self.invited_name,
            "invited_by": str(self.invited_by),
            "invite_code": self.invite_code,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_accepted": self.is_accepted,
            "accepted_at": self.accepted_at.isoformat() if self.accepted_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def is_expired(self) -> bool:
        """Check if invitation is expired."""
        return datetime.now(timezone.utc) > self.expires_at.replace(tzinfo=timezone.utc)
    
    def is_valid(self) -> bool:
        """Check if invitation is valid (not accepted and not expired)."""
        return not self.is_accepted and not self.is_expired()
