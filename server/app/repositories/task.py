"""
Task repository for database operations.

This module provides the TaskRepository class for task-specific
database operations extending the base repository functionality.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Task repository for task-specific database operations.
    
    This class extends BaseRepository to provide task-specific
    database operations and queries.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the task repository.
        
        Args:
            session: Database session
        """
        super().__init__(Task, session)
    
    async def get_by_title(self, title: str) -> Optional[Task]:
        """
        Get a task by title.
        
        Args:
            title: Task title
            
        Returns:
            Task instance or None if not found
        """
        result = await self.session.execute(
            select(Task).where(Task.title == title)
        )
        return result.scalar_one_or_none()
    
    async def get_completed_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all completed tasks.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of completed tasks
        """
        result = await self.session.execute(
            select(Task)
            .where(Task.completed == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_pending_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all pending (incomplete) tasks.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pending tasks
        """
        result = await self.session.execute(
            select(Task)
            .where(Task.completed == False)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def search_tasks(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Search tasks by title or description.
        
        Args:
            search_term: Search term to match against title or description
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching tasks
        """
        search_pattern = f"%{search_term}%"
        result = await self.session.execute(
            select(Task)
            .where(
                (Task.title.ilike(search_pattern)) |
                (Task.description.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_tasks_by_completion_status(self, completed: bool, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get tasks by completion status.
        
        Args:
            completed: Completion status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of tasks with specified completion status
        """
        result = await self.session.execute(
            select(Task)
            .where(Task.completed == completed)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def count_completed_tasks(self) -> int:
        """
        Get count of completed tasks.
        
        Returns:
            Number of completed tasks
        """
        result = await self.session.execute(
            select(Task).where(Task.completed == True)
        )
        return len(result.scalars().all())
    
    async def count_pending_tasks(self) -> int:
        """
        Get count of pending tasks.
        
        Returns:
            Number of pending tasks
        """
        result = await self.session.execute(
            select(Task).where(Task.completed == False)
        )
        return len(result.scalars().all())
