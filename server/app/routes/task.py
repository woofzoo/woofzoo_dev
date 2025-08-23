"""
Task routes for API endpoints.

This module defines all task-related API endpoints with proper
dependency injection and request/response handling.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.controllers.task import TaskController
from app.dependencies import get_task_controller
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate

# Create router
router = APIRouter(prefix="/tasks", tags=["tasks"])


# API Endpoints
@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with the provided data"
)
async def create_task(
    task_data: TaskCreate,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """
    Create a new task.
    
    Args:
        task_data: Task creation data
        controller: Task controller instance
        
    Returns:
        Created task response
    """
    return await controller.create_task(task_data)


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get all tasks",
    description="Retrieve all tasks with optional pagination and filtering"
)
async def get_tasks(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: TaskController = Depends(get_task_controller)
) -> TaskListResponse:
    """
    Get all tasks with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Task controller instance
        
    Returns:
        List of tasks with total count
    """
    return await controller.get_all_tasks(skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    description="Retrieve a specific task by its ID"
)
async def get_task(
    task_id: int,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """
    Get a task by ID.
    
    Args:
        task_id: Task ID
        controller: Task controller instance
        
    Returns:
        Task response
    """
    return await controller.get_task(task_id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task with the provided data"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """
    Update a task.
    
    Args:
        task_id: Task ID
        task_data: Task update data
        controller: Task controller instance
        
    Returns:
        Updated task response
    """
    return await controller.update_task(task_id, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task by its ID"
)
async def delete_task(
    task_id: int,
    controller: TaskController = Depends(get_task_controller)
) -> None:
    """
    Delete a task.
    
    Args:
        task_id: Task ID
        controller: Task controller instance
    """
    await controller.delete_task(task_id)


@router.get(
    "/completed/",
    response_model=TaskListResponse,
    summary="Get completed tasks",
    description="Retrieve all completed tasks with pagination"
)
async def get_completed_tasks(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: TaskController = Depends(get_task_controller)
) -> TaskListResponse:
    """
    Get all completed tasks.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Task controller instance
        
    Returns:
        List of completed tasks with total count
    """
    return await controller.get_completed_tasks(skip=skip, limit=limit)


@router.get(
    "/pending/",
    response_model=TaskListResponse,
    summary="Get pending tasks",
    description="Retrieve all pending (incomplete) tasks with pagination"
)
async def get_pending_tasks(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: TaskController = Depends(get_task_controller)
) -> TaskListResponse:
    """
    Get all pending tasks.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Task controller instance
        
    Returns:
        List of pending tasks with total count
    """
    return await controller.get_pending_tasks(skip=skip, limit=limit)


@router.get(
    "/search/",
    response_model=TaskListResponse,
    summary="Search tasks",
    description="Search tasks by title or description"
)
async def search_tasks(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: TaskController = Depends(get_task_controller)
) -> TaskListResponse:
    """
    Search tasks by title or description.
    
    Args:
        q: Search term
        skip: Number of records to skip
        limit: Maximum number of records to return
        controller: Task controller instance
        
    Returns:
        List of matching tasks with total count
    """
    return await controller.search_tasks(search_term=q, skip=skip, limit=limit)


@router.get(
    "/statistics/",
    summary="Get task statistics",
    description="Retrieve statistics about tasks (total, completed, pending, completion rate)"
)
async def get_task_statistics(
    controller: TaskController = Depends(get_task_controller)
) -> dict:
    """
    Get task statistics.
    
    Args:
        controller: Task controller instance
        
    Returns:
        Task statistics
    """
    return await controller.get_task_statistics()
