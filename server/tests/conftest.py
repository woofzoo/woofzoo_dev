"""
Pytest configuration and fixtures.

This module provides pytest fixtures and configuration for testing the application.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.database import Base, get_db_session
from app.main import app
from app.repositories.task import TaskRepository
from app.services.task import TaskService


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(test_session: AsyncSession) -> Generator:
    """Create a test client for the FastAPI application."""
    
    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_session
    
    app.dependency_overrides[get_db_session] = override_get_db_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def task_repository(test_session: AsyncSession) -> TaskRepository:
    """Create a task repository for testing."""
    return TaskRepository(test_session)


@pytest.fixture
def task_service(task_repository: TaskRepository) -> TaskService:
    """Create a task service for testing."""
    return TaskService(task_repository)


@pytest.fixture
def sample_task_data() -> dict:
    """Sample task data for testing."""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }


@pytest.fixture
def sample_task_update_data() -> dict:
    """Sample task update data for testing."""
    return {
        "title": "Updated Test Task",
        "description": "This is an updated test task",
        "completed": True
    }
