"""
User model for the application.

This module defines the User SQLAlchemy model representing users in the system.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, JSON, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    """User roles enumeration."""
    PET_OWNER = "pet_owner"
    FAMILY_MEMBER = "family_member"
    CLINIC_OWNER = "clinic_owner"
    DOCTOR = "doctor"


class User(Base):
    """
    User model representing a user in the system.
    
    Attributes:
        id: Primary key identifier
        email: User email address (unique)
        password_hash: Hashed password
        first_name: User's first name
        last_name: User's last name
        phone: User's phone number
        roles: User roles (JSON array)
        is_active: Account activation status
        is_verified: Email verification status
        email_verification_token: Token for email verification
        email_verification_expires: Email verification token expiration
        password_reset_token: Token for password reset
        password_reset_expires: Password reset token expiration
        personalization: User personalization settings (JSON)
        last_login: Last login timestamp
        created_at: User creation timestamp
        updated_at: User last update timestamp
    """
    
    __tablename__ = "users"
    
    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    password_hash: str = Column(String(255), nullable=False)
    first_name: str = Column(String(100), nullable=False)
    last_name: str = Column(String(100), nullable=False)
    phone: Optional[str] = Column(String(20), nullable=True)
    
    # Roles - stored as JSON array to support multiple roles
    roles: list[str] = Column(JSON, nullable=False, default=list)
    
    # Account status
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    
    # Email verification
    email_verification_token: Optional[str] = Column(String(255), nullable=True, index=True)
    email_verification_expires: Optional[datetime] = Column(DateTime, nullable=True)
    
    # Password reset
    password_reset_token: Optional[str] = Column(String(255), nullable=True, index=True)
    password_reset_expires: Optional[datetime] = Column(DateTime, nullable=True)
    
    # Personalization settings (JSON object)
    personalization: dict = Column(JSON, nullable=False, default=dict)
    
    # Login tracking
    last_login: Optional[datetime] = Column(DateTime, nullable=True)
    
    # Timestamps
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
        """String representation of the User model."""
        return f"<User(id={self.id}, email='{self.email}', roles={self.roles})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "roles": self.roles,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "personalization": self.personalization,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles
    
    def add_role(self, role: str) -> None:
        """Add a role to the user."""
        if role not in self.roles:
            self.roles.append(role)
    
    def remove_role(self, role: str) -> None:
        """Remove a role from the user."""
        if role in self.roles:
            self.roles.remove(role)
