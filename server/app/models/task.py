"""
Task model for the application.

This module defines the Task SQLAlchemy model representing tasks in the system.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Task(Base):
    """
    Task model representing a task in the system.
    
    Attributes:
        id: Primary key identifier
        title: Task title (required)
        description: Task description (optional)
        completed: Task completion status
        created_at: Task creation timestamp
        updated_at: Task last update timestamp
    """
    
    __tablename__ = "tasks"
    
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(255), nullable=False, index=True)
    description: Optional[str] = Column(Text, nullable=True)
    completed: bool = Column(Boolean, default=False, nullable=False)
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
        """String representation of the Task model."""
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
