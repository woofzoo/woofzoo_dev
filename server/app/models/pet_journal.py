"""
Pet Journal model for the application.

This module defines the PetJournal SQLAlchemy model representing
journal entries for pets made by owners.
"""

from datetime import datetime, date
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, Date, String, Text, UUID, ForeignKey, JSON
from sqlalchemy.sql import func

from app.database import Base


class PetJournal(Base):
    """
    Pet Journal model representing journal entries for pets.
    
    This model allows pet owners to log daily activities, medication given,
    events, and health observations for their pets.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: ID of the pet this entry is for
        created_by_user_id: ID of the user who created the entry
        entry_type: Type of journal entry (daily_activity, medication_given, activity_event, health_note)
        title: Brief title/summary of the entry
        content: Detailed content of the journal entry
        entry_date: Date the activity/event occurred
        metadata: JSON object for flexible additional data
        created_at: Entry creation timestamp
        updated_at: Entry last update timestamp
    """
    
    __tablename__ = "pet_journals"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    created_by_user_id: int = Column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    # Entry classification
    entry_type: str = Column(String(50), nullable=False, index=True)
    
    # Entry content
    title: str = Column(String(200), nullable=False)
    content: str = Column(Text, nullable=False)
    entry_date: date = Column(Date, nullable=False, index=True)
    
    # Flexible metadata for additional information
    metadata: dict = Column(JSON, nullable=False, default=dict)
    
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
        """String representation of the PetJournal model."""
        return f"<PetJournal(id={self.id}, pet_id={self.pet_id}, entry_type='{self.entry_type}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": str(self.pet_id),
            "created_by_user_id": self.created_by_user_id,
            "entry_type": self.entry_type,
            "title": self.title,
            "content": self.content,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

