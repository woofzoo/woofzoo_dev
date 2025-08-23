"""
User service for business logic operations.

This module provides the UserService class for user-related business logic,
demonstrating complex service dependencies.
"""

from typing import List, Optional

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.task import TaskService
from app.services.notification import NotificationService
from app.services.email import EmailService


class UserService:
    """
    User service for business logic operations.
    
    This class demonstrates complex service dependencies and how they
    can be managed through centralized dependency injection.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        task_service: TaskService,
        notification_service: NotificationService,
        email_service: EmailService
    ) -> None:
        """
        Initialize the user service with multiple dependencies.
        
        Args:
            user_repository: User repository instance
            task_service: Task service instance
            notification_service: Notification service instance
            email_service: Email service instance
        """
        self.user_repository = user_repository
        self.task_service = task_service
        self.notification_service = notification_service
        self.email_service = email_service
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user with complex business logic.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user instance
        """
        # Check if user with same email already exists
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"User with email '{user_data.email}' already exists")
        
        # Create the user
        user = await self.user_repository.create(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name
        )
        
        # Send welcome email
        await self.email_service.send_welcome_email(user.email, user.full_name)
        
        # Send welcome notification
        await self.notification_service.send_welcome_notification(user.id)
        
        # Create default tasks for new user
        await self._create_default_tasks(user.id)
        
        return user
    
    async def get_user_with_tasks(self, user_id: int) -> Optional[dict]:
        """
        Get user with their associated tasks.
        
        Args:
            user_id: User ID
            
        Returns:
            User with tasks or None if not found
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        # Get user's tasks
        tasks = await self.task_service.get_tasks_by_user_id(user_id)
        
        return {
            "user": user,
            "tasks": tasks,
            "task_count": len(tasks)
        }
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user with cleanup operations.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False if not found
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return False
        
        # Delete all user's tasks
        await self.task_service.delete_tasks_by_user_id(user_id)
        
        # Send goodbye email
        await self.email_service.send_goodbye_email(user.email, user.full_name)
        
        # Delete user
        deleted = await self.user_repository.delete(user_id)
        
        if deleted:
            # Send notification to admin
            await self.notification_service.send_user_deletion_notification(user_id)
        
        return deleted
    
    async def _create_default_tasks(self, user_id: int) -> None:
        """
        Create default tasks for new user.
        
        Args:
            user_id: User ID
        """
        default_tasks = [
            {
                "title": "Welcome to WoofZoo!",
                "description": "This is your first task. Start exploring the platform!",
                "user_id": user_id
            },
            {
                "title": "Complete your profile",
                "description": "Add your profile picture and update your information",
                "user_id": user_id
            }
        ]
        
        for task_data in default_tasks:
            await self.task_service.create_task_for_user(user_id, task_data)
