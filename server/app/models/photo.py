"""
Photo model for the application.

This module defines the Photo SQLAlchemy model for storing photo metadata
and references to cloud storage.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class Photo(Base):
    """
    Photo model representing a photo in the system.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: Associated pet's unique identifier
        filename: Original filename
        file_path: Path in cloud storage (S3)
        file_size: File size in bytes
        mime_type: MIME type of the file
        width: Image width in pixels
        height: Image height in pixels
        is_primary: Whether this is the primary photo for the pet
        is_active: Whether the photo is active/visible
        uploaded_by: User who uploaded the photo
        created_at: Photo creation timestamp
        updated_at: Photo last update timestamp
    """
    
    __tablename__ = "photos"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    filename: str = Column(String(255), nullable=False)
    file_path: str = Column(String(500), nullable=False)
    file_size: int = Column(Integer, nullable=False)
    mime_type: str = Column(String(100), nullable=False)
    width: Optional[int] = Column(Integer, nullable=True)
    height: Optional[int] = Column(Integer, nullable=True)
    is_primary: bool = Column(Boolean, default=False, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    uploaded_by: Optional[int] = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the Photo model."""
        return f"<Photo(id={self.id}, filename='{self.filename}', pet_id={self.pet_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": str(self.pet_id),
            "filename": self.filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "width": self.width,
            "height": self.height,
            "is_primary": self.is_primary,
            "is_active": self.is_active,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
