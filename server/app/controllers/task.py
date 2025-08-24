"""
Task controller for API layer.

This module provides the TaskController class for handling HTTP requests
and responses related to task operations.
"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.services.task import TaskService


class TaskController:
    """
    Task controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to task operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, task_service: TaskService) -> None:
        """
        Initialize the task controller.
        
        Args:
            task_service: Task service instance
        """
        self.task_service = task_service
    
    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """
        Create a new task.
        
        Args:
            task_data: Task creation data
            
        Returns:
            Created task response
            
        Raises:
            HTTPException: If task creation fails
        """
        try:
            task = await self.task_service.create_task(task_data)
            return TaskResponse.model_validate(task.to_dict())
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create task"
            )
    
    async def get_task(self, task_id: int) -> TaskResponse:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task response
            
        Raises:
            HTTPException: If task not found
        """
        task = await self.task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        
        return TaskResponse.model_validate(task.to_dict())
    
    async def get_all_tasks(self, skip: int = 0, limit: int = 100) -> TaskListResponse:
        """
        Get all tasks with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of task responses with total count
        """
        try:
            tasks = await self.task_service.get_all_tasks(skip=skip, limit=limit)
            total = await self.task_service.task_repository.count()
            
            task_responses = [TaskResponse.model_validate(task.to_dict()) for task in tasks]
            return TaskListResponse(tasks=task_responses, total=total)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve tasks"
            )
    
    async def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        """
        Update a task.
        
        Args:
            task_id: Task ID
            task_data: Task update data
            
        Returns:
            Updated task response
            
        Raises:
            HTTPException: If task not found or update fails
        """
        try:
            task = await self.task_service.update_task(task_id, task_data)
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task with ID {task_id} not found"
                )
            
            return TaskResponse.model_validate(task.to_dict())
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update task"
            )
    
    async def delete_task(self, task_id: int) -> dict:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If task not found or deletion fails
        """
        try:
            deleted = await self.task_service.delete_task(task_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task with ID {task_id} not found"
                )
            
            return {"message": f"Task with ID {task_id} deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete task"
            )
    
    async def get_completed_tasks(self, skip: int = 0, limit: int = 100) -> TaskListResponse:
        """
        Get all completed tasks.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of completed task responses with total count
        """
        try:
            tasks = await self.task_service.get_completed_tasks(skip=skip, limit=limit)
            total = await self.task_service.task_repository.count_completed_tasks()
            
            task_responses = [TaskResponse.model_validate(task.to_dict()) for task in tasks]
            return TaskListResponse(tasks=task_responses, total=total)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve completed tasks"
            )
    
    async def get_pending_tasks(self, skip: int = 0, limit: int = 100) -> TaskListResponse:
        """
        Get all pending tasks.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pending task responses with total count
        """
        try:
            tasks = await self.task_service.get_pending_tasks(skip=skip, limit=limit)
            total = await self.task_service.task_repository.count_pending_tasks()
            
            task_responses = [TaskResponse.model_validate(task.to_dict()) for task in tasks]
            return TaskListResponse(tasks=task_responses, total=total)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve pending tasks"
            )
    
    async def search_tasks(self, search_term: str, skip: int = 0, limit: int = 100) -> TaskListResponse:
        """
        Search tasks by title or description.
        
        Args:
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching task responses with total count
        """
        try:
            tasks = await self.task_service.search_tasks(
                search_term=search_term,
                skip=skip,
                limit=limit
            )
            
            task_responses = [TaskResponse.model_validate(task.to_dict()) for task in tasks]
            return TaskListResponse(tasks=task_responses, total=len(task_responses))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search tasks"
            )
    
    async def get_task_statistics(self) -> dict:
        """
        Get task statistics.
        
        Returns:
            Task statistics
        """
        try:
            return await self.task_service.get_task_statistics()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve task statistics"
            )
