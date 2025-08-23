"""
User repository for database operations.

This module provides the UserRepository class for user-specific
database operations extending the base repository functionality.
"""

from typing import List, Optional
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository for user-specific database operations.
    
    This class extends BaseRepository to provide user-specific
    database operations and queries.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize the user repository."""
        super().__init__(User, session)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_verification_token(self, token: str) -> Optional[User]:
        """Get a user by email verification token."""
        result = await self.session.execute(
            select(User).where(User.email_verification_token == token)
        )
        return result.scalar_one_or_none()
    
    async def get_by_reset_token(self, token: str) -> Optional[User]:
        """Get a user by password reset token."""
        result = await self.session.execute(
            select(User).where(User.password_reset_token == token)
        )
        return result.scalar_one_or_none()
    
    async def get_users_by_role(self, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role with pagination."""
        result = await self.session.execute(
            select(User)
            .where(User.roles.contains([role]))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by name or email."""
        search_pattern = f"%{search_term}%"
        result = await self.session.execute(
            select(User)
            .where(
                (User.first_name.ilike(search_pattern)) |
                (User.last_name.ilike(search_pattern)) |
                (User.email.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp."""
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login=datetime.utcnow())
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def update_verification_token(
        self,
        user_id: int,
        token: str,
        expires_at: datetime
    ) -> bool:
        """Update user's email verification token."""
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                email_verification_token=token,
                email_verification_expires=expires_at
            )
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def update_reset_token(
        self,
        user_id: int,
        token: str,
        expires_at: datetime
    ) -> bool:
        """Update user's password reset token."""
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                password_reset_token=token,
                password_reset_expires=expires_at
            )
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def clear_verification_token(self, user_id: int) -> bool:
        """Clear user's email verification token."""
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                email_verification_token=None,
                email_verification_expires=None,
                is_verified=True
            )
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def clear_reset_token(self, user_id: int) -> bool:
        """Clear user's password reset token."""
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                password_reset_token=None,
                password_reset_expires=None
            )
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def update_personalization(self, user_id: int, personalization: dict) -> bool:
        """Update user's personalization settings."""
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(personalization=personalization)
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def add_role(self, user_id: int, role: str) -> bool:
        """Add a role to a user."""
        user = await self.get_by_id(user_id)
        if user:
            user.add_role(role)
            await self.session.commit()
            return True
        return False
    
    async def remove_role(self, user_id: int, role: str) -> bool:
        """Remove a role from a user."""
        user = await self.get_by_id(user_id)
        if user:
            user.remove_role(role)
            await self.session.commit()
            return True
        return False
    
    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users with pagination."""
        result = await self.session.execute(
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_verified_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all verified users with pagination."""
        result = await self.session.execute(
            select(User)
            .where(User.is_verified == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def count_by_role(self, role: str) -> int:
        """Count users with a specific role."""
        result = await self.session.execute(
            select(User).where(User.roles.contains([role]))
        )
        return len(result.scalars().all())
    
    async def count_active_users(self) -> int:
        """Count active users."""
        result = await self.session.execute(
            select(User).where(User.is_active == True)
        )
        return len(result.scalars().all())
    
    async def count_verified_users(self) -> int:
        """Count verified users."""
        result = await self.session.execute(
            select(User).where(User.is_verified == True)
        )
        return len(result.scalars().all())
