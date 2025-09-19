"""
OTP model for the application.

This module defines the OTP SQLAlchemy model for managing OTP codes
used for authentication and family invitations.
"""

from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, String, Boolean, UUID, ForeignKey, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


class OTPPurpose(str, enum.Enum):
    """OTP purpose enumeration."""
    LOGIN = "login"
    FAMILY_INVITE = "family_invite"
    PET_ACCESS = "pet_access"


class OTP(Base):
    """
    OTP model representing an OTP code in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        phone_number: Phone number the OTP was sent to
        otp_code: 6-digit OTP code
        purpose: Purpose of the OTP (login, family_invite, pet_access)
        expires_at: When the OTP expires
        is_used: Whether the OTP has been used
        created_at: OTP creation timestamp
    """
    
    __tablename__ = "otps"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number: str = Column(String(15), nullable=False, index=True)
    otp_code: str = Column(String(6), nullable=False)
    purpose: str = Column(Enum(OTPPurpose), nullable=False)
    expires_at: datetime = Column(DateTime, nullable=False)
    is_used: bool = Column(Boolean, default=False, nullable=False)
    created_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the OTP model."""
        return f"<OTP(id={self.id}, phone='{self.phone_number}', purpose='{self.purpose}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "phone_number": self.phone_number,
            "otp_code": self.otp_code,
            "purpose": self.purpose.value if self.purpose else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_used": self.is_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def is_expired(self) -> bool:
        """Check if OTP is expired."""
        return datetime.now(timezone.utc).replace(tzinfo=None) > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if OTP is valid (not used and not expired)."""
        return not self.is_used and not self.is_expired()
