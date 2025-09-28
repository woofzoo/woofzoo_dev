"""
Family model for the application.

This module defines the Family SQLAlchemy model representing family groups in the system.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, String, Text, Boolean, UUID, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Family(Base):
    """
    Family model representing a family group in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        name: Family name
        admin_owner_id: ID of the owner who administers this family
        description: Optional family description
        created_at: Family creation timestamp
        updated_at: Family last update timestamp
    """
    
    __tablename__ = "families"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String(100), nullable=False)
    # Admin user (UUID) references users.public_id
    admin_owner_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.public_id"), nullable=False)
    description: Optional[str] = Column(Text, nullable=True)
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
        """String representation of the Family model."""
        return f"<Family(id={self.id}, name='{self.name}', admin_owner_id={self.admin_owner_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "admin_owner_id": str(self.admin_owner_id),
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
