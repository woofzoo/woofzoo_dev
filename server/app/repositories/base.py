"""
Base repository for database operations.

This module provides the BaseRepository class that serves as the foundation
for all repository classes, providing common database operations.
"""

import uuid
from typing import Any, Generic, List, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository for common database operations.
    
    This class provides basic CRUD operations that can be extended
    by specific repository classes for domain-specific operations.
    """
    
    def __init__(self, model: type[ModelType], session: Session) -> None:
        """
        Initialize the base repository.
        
        Args:
            model: SQLAlchemy model class
            session: Database session
        """
        self.model = model
        self.session = session
    
    def create(self, **kwargs: Any) -> ModelType:
        """
        Create a new record.
        
        Args:
            **kwargs: Model attributes
            
        Returns:
            Created model instance
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def get_by_id(self, id: str) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            id: Record ID (UUID string)
            
        Returns:
            Model instance or None if not found
        """
        try:
            # Convert string ID to UUID if needed
            if isinstance(id, str):
                id = uuid.UUID(id)
            
            result = self.session.execute(
                select(self.model).where(self.model.id == id)
            )
            return result.scalar_one_or_none()
        except (ValueError, AttributeError):
            # Invalid UUID format
            return None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        result = self.session.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def update(self, id: str, **kwargs: Any) -> Optional[ModelType]:
        """
        Update a record by ID.
        
        Args:
            id: Record ID (UUID string)
            **kwargs: Model attributes to update
            
        Returns:
            Updated model instance or None if not found
        """
        try:
            # Convert string ID to UUID if needed
            if isinstance(id, str):
                id = uuid.UUID(id)
            
            instance = self.get_by_id(id)
            if instance:
                for key, value in kwargs.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)
                self.session.commit()
                self.session.refresh(instance)
            return instance
        except (ValueError, AttributeError):
            # Invalid UUID format
            return None
    
    def delete(self, id: str) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID (UUID string)
            
        Returns:
            True if deleted, False if not found
        """
        try:
            # Convert string ID to UUID if needed
            if isinstance(id, str):
                id = uuid.UUID(id)
            
            instance = self.get_by_id(id)
            if instance:
                self.session.delete(instance)
                self.session.commit()
                return True
            return False
        except (ValueError, AttributeError):
            # Invalid UUID format
            return False
    
    def count(self) -> int:
        """
        Get total count of records.
        
        Returns:
            Total number of records
        """
        result = self.session.execute(select(self.model))
        return len(result.scalars().all())
