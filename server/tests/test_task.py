"""
Tests for task functionality.

This module contains tests for task-related functionality including
API endpoints, service layer, and repository layer.
"""

import pytest
from fastapi import status

from app.schemas.task import TaskCreate, TaskUpdate


class TestTaskAPI:
    """Test cases for task API endpoints."""
    
    def test_create_task_success(self, client, sample_task_data):
        """Test successful task creation."""
        response = client.post("/api/tasks/", json=sample_task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["completed"] == sample_task_data["completed"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_task_duplicate_title(self, client, sample_task_data):
        """Test task creation with duplicate title."""
        # Create first task
        client.post("/api/tasks/", json=sample_task_data)
        
        # Try to create second task with same title
        response = client.post("/api/tasks/", json=sample_task_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_get_task_success(self, client, sample_task_data):
        """Test successful task retrieval."""
        # Create a task first
        create_response = client.post("/api/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Get the task
        response = client.get(f"/api/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == sample_task_data["title"]
    
    def test_get_task_not_found(self, client):
        """Test task retrieval with non-existent ID."""
        response = client.get("/api/tasks/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_all_tasks(self, client, sample_task_data):
        """Test retrieving all tasks."""
        # Create multiple tasks
        client.post("/api/tasks/", json=sample_task_data)
        client.post("/api/tasks/", json={"title": "Task 2", "description": "Second task"})
        
        response = client.get("/api/tasks/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert len(data["tasks"]) >= 2
        assert data["total"] >= 2
    
    def test_update_task_success(self, client, sample_task_data, sample_task_update_data):
        """Test successful task update."""
        # Create a task first
        create_response = client.post("/api/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Update the task
        response = client.put(f"/api/tasks/{task_id}", json=sample_task_update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == sample_task_update_data["title"]
        assert data["description"] == sample_task_update_data["description"]
        assert data["completed"] == sample_task_update_data["completed"]
    
    def test_update_task_not_found(self, client, sample_task_update_data):
        """Test task update with non-existent ID."""
        response = client.put("/api/tasks/999", json=sample_task_update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_delete_task_success(self, client, sample_task_data):
        """Test successful task deletion."""
        # Create a task first
        create_response = client.post("/api/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/api/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_task_not_found(self, client):
        """Test task deletion with non-existent ID."""
        response = client.delete("/api/tasks/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_completed_tasks(self, client, sample_task_data):
        """Test retrieving completed tasks."""
        # Create a completed task
        completed_task = sample_task_data.copy()
        completed_task["completed"] = True
        client.post("/api/tasks/", json=completed_task)
        
        response = client.get("/api/tasks/completed/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert all(task["completed"] for task in data["tasks"])
    
    def test_get_pending_tasks(self, client, sample_task_data):
        """Test retrieving pending tasks."""
        # Create a pending task
        client.post("/api/tasks/", json=sample_task_data)
        
        response = client.get("/api/tasks/pending/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert all(not task["completed"] for task in data["tasks"])
    
    def test_search_tasks(self, client, sample_task_data):
        """Test searching tasks."""
        # Create a task
        client.post("/api/tasks/", json=sample_task_data)
        
        response = client.get("/api/tasks/search/?q=Test")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert len(data["tasks"]) > 0
    
    def test_get_task_statistics(self, client, sample_task_data):
        """Test retrieving task statistics."""
        # Create some tasks
        client.post("/api/tasks/", json=sample_task_data)
        completed_task = sample_task_data.copy()
        completed_task["title"] = "Completed Task"
        completed_task["completed"] = True
        client.post("/api/tasks/", json=completed_task)
        
        response = client.get("/api/tasks/statistics/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_tasks" in data
        assert "completed_tasks" in data
        assert "pending_tasks" in data
        assert "completion_rate" in data
        assert data["total_tasks"] >= 2


class TestTaskService:
    """Test cases for task service layer."""
    
    @pytest.mark.asyncio
    async def test_create_task_success(self, task_service, sample_task_data):
        """Test successful task creation in service layer."""
        task_create = TaskCreate(**sample_task_data)
        task = await task_service.create_task(task_create)
        
        assert task.title == sample_task_data["title"]
        assert task.description == sample_task_data["description"]
        assert task.completed == sample_task_data["completed"]
        assert task.id is not None
    
    @pytest.mark.asyncio
    async def test_create_task_duplicate_title(self, task_service, sample_task_data):
        """Test task creation with duplicate title in service layer."""
        task_create = TaskCreate(**sample_task_data)
        
        # Create first task
        await task_service.create_task(task_create)
        
        # Try to create second task with same title
        with pytest.raises(ValueError, match="already exists"):
            await task_service.create_task(task_create)
    
    @pytest.mark.asyncio
    async def test_get_task_by_id(self, task_service, sample_task_data):
        """Test getting task by ID in service layer."""
        task_create = TaskCreate(**sample_task_data)
        created_task = await task_service.create_task(task_create)
        
        retrieved_task = await task_service.get_task_by_id(created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title
    
    @pytest.mark.asyncio
    async def test_get_task_by_id_not_found(self, task_service):
        """Test getting non-existent task by ID in service layer."""
        task = await task_service.get_task_by_id(999)
        
        assert task is None
    
    @pytest.mark.asyncio
    async def test_update_task_success(self, task_service, sample_task_data, sample_task_update_data):
        """Test successful task update in service layer."""
        task_create = TaskCreate(**sample_task_data)
        created_task = await task_service.create_task(task_create)
        
        task_update = TaskUpdate(**sample_task_update_data)
        updated_task = await task_service.update_task(created_task.id, task_update)
        
        assert updated_task is not None
        assert updated_task.title == sample_task_update_data["title"]
        assert updated_task.description == sample_task_update_data["description"]
        assert updated_task.completed == sample_task_update_data["completed"]
    
    @pytest.mark.asyncio
    async def test_delete_task_success(self, task_service, sample_task_data):
        """Test successful task deletion in service layer."""
        task_create = TaskCreate(**sample_task_data)
        created_task = await task_service.create_task(task_create)
        
        deleted = await task_service.delete_task(created_task.id)
        
        assert deleted is True
        
        # Verify task is deleted
        retrieved_task = await task_service.get_task_by_id(created_task.id)
        assert retrieved_task is None
    
    @pytest.mark.asyncio
    async def test_get_task_statistics(self, task_service, sample_task_data):
        """Test getting task statistics in service layer."""
        # Create some tasks
        task_create = TaskCreate(**sample_task_data)
        await task_service.create_task(task_create)
        
        completed_task = TaskCreate(
            title="Completed Task",
            description="A completed task",
            completed=True
        )
        await task_service.create_task(completed_task)
        
        stats = await task_service.get_task_statistics()
        
        assert "total_tasks" in stats
        assert "completed_tasks" in stats
        assert "pending_tasks" in stats
        assert "completion_rate" in stats
        assert stats["total_tasks"] >= 2


class TestTaskRepository:
    """Test cases for task repository layer."""
    
    @pytest.mark.asyncio
    async def test_create_task(self, task_repository, sample_task_data):
        """Test task creation in repository layer."""
        task = await task_repository.create(**sample_task_data)
        
        assert task.title == sample_task_data["title"]
        assert task.description == sample_task_data["description"]
        assert task.completed == sample_task_data["completed"]
        assert task.id is not None
    
    @pytest.mark.asyncio
    async def test_get_by_id(self, task_repository, sample_task_data):
        """Test getting task by ID in repository layer."""
        created_task = await task_repository.create(**sample_task_data)
        
        retrieved_task = await task_repository.get_by_id(created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title
    
    @pytest.mark.asyncio
    async def test_get_all_tasks(self, task_repository, sample_task_data):
        """Test getting all tasks in repository layer."""
        await task_repository.create(**sample_task_data)
        await task_repository.create(title="Task 2", description="Second task")
        
        tasks = await task_repository.get_all()
        
        assert len(tasks) >= 2
        assert any(task.title == sample_task_data["title"] for task in tasks)
        assert any(task.title == "Task 2" for task in tasks)
    
    @pytest.mark.asyncio
    async def test_update_task(self, task_repository, sample_task_data, sample_task_update_data):
        """Test updating task in repository layer."""
        created_task = await task_repository.create(**sample_task_data)
        
        updated_task = await task_repository.update(created_task.id, **sample_task_update_data)
        
        assert updated_task is not None
        assert updated_task.title == sample_task_update_data["title"]
        assert updated_task.description == sample_task_update_data["description"]
        assert updated_task.completed == sample_task_update_data["completed"]
    
    @pytest.mark.asyncio
    async def test_delete_task(self, task_repository, sample_task_data):
        """Test deleting task in repository layer."""
        created_task = await task_repository.create(**sample_task_data)
        
        deleted = await task_repository.delete(created_task.id)
        
        assert deleted is True
        
        # Verify task is deleted
        retrieved_task = await task_repository.get_by_id(created_task.id)
        assert retrieved_task is None
