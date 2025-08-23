"""
Task Pydantic schemas for request/response validation.

This module defines Pydantic models for task-related API operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base Task schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: bool = Field(default=False, description="Task completion status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Learn FastAPI",
                "description": "Study clean architecture principles",
                "completed": False
            }
        }
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: Optional[bool] = Field(None, description="Task completion status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Learn FastAPI",
                "description": "Study clean architecture principles",
                "completed": True
            }
        }
    )


class TaskResponse(TaskBase):
    """Schema for task response."""
    
    id: int = Field(..., description="Task unique identifier")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Learn FastAPI",
                "description": "Study clean architecture principles",
                "completed": False,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
    )


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""
    
    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "title": "Learn FastAPI",
                        "description": "Study clean architecture principles",
                        "completed": False,
                        "created_at": "2024-01-01T12:00:00Z",
                        "updated_at": "2024-01-01T12:00:00Z"
                    }
                ],
                "total": 1
            }
        }
    )
