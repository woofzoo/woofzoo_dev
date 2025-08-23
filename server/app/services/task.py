"""
Task service for business logic operations.

This module provides the TaskService class for task-related business logic,
acting as an intermediary between controllers and repositories.
"""

from typing import List, Optional

from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """
    Task service for business logic operations.
    
    This class handles business logic for task operations, including
    validation, business rules, and coordination between repositories.
    """
    
    def __init__(self, task_repository: TaskRepository) -> None:
        """
        Initialize the task service.
        
        Args:
            task_repository: Task repository instance
        """
        self.task_repository = task_repository
    
    async def create_task(self, task_data: TaskCreate) -> Task:
        """
        Create a new task with business logic validation.
        
        Args:
            task_data: Task creation data
            
        Returns:
            Created task instance
            
        Raises:
            ValueError: If task with same title already exists
        """
        # Check if task with same title already exists
        existing_task = await self.task_repository.get_by_title(task_data.title)
        if existing_task:
            raise ValueError(f"Task with title '{task_data.title}' already exists")
        
        # Create the task
        task = await self.task_repository.create(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed
        )
        
        return task
    
    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task instance or None if not found
        """
        return await self.task_repository.get_by_id(task_id)
    
    async def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all tasks with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of task instances
        """
        return await self.task_repository.get_all(skip=skip, limit=limit)
    
    async def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a task with business logic validation.
        
        Args:
            task_id: Task ID
            task_data: Task update data
            
        Returns:
            Updated task instance or None if not found
            
        Raises:
            ValueError: If task with same title already exists (when updating title)
        """
        # Check if task exists
        existing_task = await self.task_repository.get_by_id(task_id)
        if not existing_task:
            return None
        
        # If title is being updated, check for duplicates
        if task_data.title and task_data.title != existing_task.title:
            duplicate_task = await self.task_repository.get_by_title(task_data.title)
            if duplicate_task:
                raise ValueError(f"Task with title '{task_data.title}' already exists")
        
        # Prepare update data
        update_data = {}
        if task_data.title is not None:
            update_data["title"] = task_data.title
        if task_data.description is not None:
            update_data["description"] = task_data.description
        if task_data.completed is not None:
            update_data["completed"] = task_data.completed
        
        # Update the task
        return await self.task_repository.update(task_id, **update_data)
    
    async def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if deleted, False if not found
        """
        return await self.task_repository.delete(task_id)
    
    async def get_completed_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all completed tasks.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of completed task instances
        """
        return await self.task_repository.get_completed_tasks(skip=skip, limit=limit)
    
    async def get_pending_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all pending (incomplete) tasks.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pending task instances
        """
        return await self.task_repository.get_pending_tasks(skip=skip, limit=limit)
    
    async def search_tasks(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Search tasks by title or description.
        
        Args:
            search_term: Search term to match against title or description
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching task instances
        """
        if not search_term.strip():
            return await self.get_all_tasks(skip=skip, limit=limit)
        
        return await self.task_repository.search_tasks(
            search_term=search_term.strip(),
            skip=skip,
            limit=limit
        )
    
    async def get_task_statistics(self) -> dict:
        """
        Get task statistics.
        
        Returns:
            Dictionary with task statistics
        """
        total_tasks = await self.task_repository.count()
        completed_tasks = await self.task_repository.count_completed_tasks()
        pending_tasks = await self.task_repository.count_pending_tasks()
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": round(completion_rate, 2)
        }
