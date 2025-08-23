"""
Base repository class with common CRUD operations.

This module provides a base repository class that implements common
database operations using SQLAlchemy async session.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository class with common CRUD operations.
    
    This class provides a foundation for all repository classes with
    common database operations like create, read, update, delete.
    """
    
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        """
        Initialize the repository.
        
        Args:
            model: SQLAlchemy model class
            session: Database session
        """
        self.model = model
        self.session = session
    
    async def create(self, **kwargs: Any) -> ModelType:
        """
        Create a new record.
        
        Args:
            **kwargs: Model attributes
            
        Returns:
            Created model instance
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        result = await self.session.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def update(self, id: int, **kwargs: Any) -> Optional[ModelType]:
        """
        Update a record by ID.
        
        Args:
            id: Record ID
            **kwargs: Model attributes to update
            
        Returns:
            Updated model instance or None if not found
        """
        instance = await self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            await self.session.commit()
            await self.session.refresh(instance)
        return instance
    
    async def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
            return True
        return False
    
    async def count(self) -> int:
        """
        Get total count of records.
        
        Returns:
            Total number of records
        """
        result = await self.session.execute(select(self.model))
        return len(result.scalars().all())
