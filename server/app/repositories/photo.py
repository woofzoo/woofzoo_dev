"""
Photo repository for database operations.

This module provides the PhotoRepository class for photo-specific
database operations extending the base repository functionality.
"""

from typing import List, Optional
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.photo import Photo
from app.repositories.base import BaseRepository


class PhotoRepository(BaseRepository[Photo]):
    """
    Photo repository for photo-specific database operations.
    
    This class extends BaseRepository to provide photo-specific
    database operations and queries.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize the photo repository."""
        super().__init__(Photo, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[Photo]:
        """Get photos by pet ID."""
        try:
            pet_id_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            return []
        
        result = self.session.execute(
            select(Photo)
            .where(Photo.pet_id == pet_id_uuid)
            .where(Photo.is_active == True)
            .order_by(Photo.is_primary.desc(), Photo.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_primary_photo(self, pet_id: str) -> Optional[Photo]:
        """Get the primary photo for a pet."""
        try:
            pet_id_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            return None
        
        result = self.session.execute(
            select(Photo)
            .where(Photo.pet_id == pet_id_uuid)
            .where(Photo.is_primary == True)
            .where(Photo.is_active == True)
        )
        return result.scalar_one_or_none()
    
    def get_by_uploaded_by(self, uploaded_by: str, skip: int = 0, limit: int = 100) -> List[Photo]:
        """Get photos by uploader."""
        result = self.session.execute(
            select(Photo)
            .where(Photo.uploaded_by == uploaded_by)
            .where(Photo.is_active == True)
            .order_by(Photo.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def count_by_pet(self, pet_id: str) -> int:
        """Count photos by pet ID."""
        try:
            pet_id_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            return 0
        
        result = self.session.execute(
            select(Photo)
            .where(Photo.pet_id == pet_id_uuid)
            .where(Photo.is_active == True)
        )
        return len(result.scalars().all())
    
    def count_by_uploaded_by(self, uploaded_by: str) -> int:
        """Count photos by uploader."""
        result = self.session.execute(
            select(Photo)
            .where(Photo.uploaded_by == uploaded_by)
            .where(Photo.is_active == True)
        )
        return len(result.scalars().all())
    
    def set_primary_photo(self, pet_id: str, photo_id: str) -> bool:
        """Set a photo as primary for a pet (unset others)."""
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            photo_id_uuid = uuid.UUID(photo_id)
        except (ValueError, AttributeError):
            return False
        
        # First, unset all primary photos for this pet
        self.session.execute(
            select(Photo)
            .where(Photo.pet_id == pet_id_uuid)
            .where(Photo.is_primary == True)
        ).scalars().all()
        
        # Update all photos for this pet to set is_primary=False
        self.session.execute(
            Photo.__table__.update()
            .where(Photo.pet_id == pet_id_uuid)
            .values(is_primary=False)
        )
        
        # Set the specified photo as primary
        result = self.session.execute(
            Photo.__table__.update()
            .where(Photo.id == photo_id_uuid)
            .where(Photo.pet_id == pet_id_uuid)
            .values(is_primary=True)
        )
        
        return result.rowcount > 0
    
    def get_by_filename(self, pet_id: str, filename: str) -> Optional[Photo]:
        """Get photo by pet ID and filename."""
        try:
            pet_id_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            return None
        
        result = self.session.execute(
            select(Photo)
            .where(Photo.pet_id == pet_id_uuid)
            .where(Photo.filename == filename)
            .where(Photo.is_active == True)
        )
        return result.scalar_one_or_none()
    
    def get_active_photos(self, skip: int = 0, limit: int = 100) -> List[Photo]:
        """Get all active photos."""
        result = self.session.execute(
            select(Photo)
            .where(Photo.is_active == True)
            .order_by(Photo.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
