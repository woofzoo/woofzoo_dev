"""
Photo service for business logic operations.

This module provides the PhotoService class for photo-related business logic,
acting as an intermediary between controllers and repositories.
"""

from typing import List, Optional, Tuple
import uuid

from app.models.photo import Photo
from app.repositories.photo import PhotoRepository
from app.services.storage import StorageService
from app.schemas.photo import PhotoCreate, PhotoUpdate, PhotoUploadRequest


class PhotoService:
    """
    Photo service for business logic operations.
    
    This class handles business logic for photo operations, including
    validation, business rules, and coordination between repositories
    and storage services.
    """
    
    def __init__(self, photo_repository: PhotoRepository, storage_service: StorageService) -> None:
        """Initialize the photo service."""
        self.photo_repository = photo_repository
        self.storage_service = storage_service
    
    def create_photo_upload_request(self, pet_id: str, upload_request: PhotoUploadRequest, uploaded_by: Optional[int] = None) -> Tuple[Photo, str]:
        """
        Create a photo record and generate upload URL.
        
        Args:
            pet_id: Pet's unique identifier
            upload_request: Photo upload request data
            uploaded_by: User who is uploading the photo
            
        Returns:
            Tuple of (Photo object, upload URL)
        """
        # Validate upload request
        is_valid, error_message = self.storage_service.validate_upload_request(
            upload_request.filename,
            upload_request.file_size,
            upload_request.mime_type
        )
        
        if not is_valid:
            raise ValueError(error_message)
        
        # Generate file path
        file_path = self.storage_service._generate_file_path(pet_id, upload_request.filename)
        
        # Create photo record
        photo_data = {
            "pet_id": pet_id,
            "filename": upload_request.filename,
            "file_path": file_path,
            "file_size": upload_request.file_size,
            "mime_type": upload_request.mime_type,
            "is_primary": upload_request.is_primary
        }
        
        if uploaded_by:
            photo_data["uploaded_by"] = uploaded_by
        
        photo = self.photo_repository.create(**photo_data)
        
        # If this is set as primary, unset other primary photos
        if upload_request.is_primary:
            self.photo_repository.set_primary_photo(pet_id, str(photo.id))
        
        # Generate upload URL
        upload_url = self.storage_service.create_upload_url(
            file_path,
            upload_request.mime_type,
            expires_in=3600  # 1 hour
        )
        
        return photo, upload_url
    
    def create_photo(self, photo_data: PhotoCreate) -> Photo:
        """Create a new photo with business logic validation."""
        # Validate upload request
        is_valid, error_message = self.storage_service.validate_upload_request(
            photo_data.filename,
            photo_data.file_size,
            photo_data.mime_type
        )
        
        if not is_valid:
            raise ValueError(error_message)
        
        # Generate file path
        file_path = self.storage_service._generate_file_path(photo_data.pet_id, photo_data.filename)
        
        # Create photo record
        photo = self.photo_repository.create(
            pet_id=photo_data.pet_id,
            filename=photo_data.filename,
            file_path=file_path,
            file_size=photo_data.file_size,
            mime_type=photo_data.mime_type,
            width=photo_data.width,
            height=photo_data.height,
            is_primary=photo_data.is_primary,
            uploaded_by=photo_data.uploaded_by
        )
        
        # If this is set as primary, unset other primary photos
        if photo_data.is_primary:
            self.photo_repository.set_primary_photo(photo_data.pet_id, str(photo.id))
        
        return photo
    
    def get_photo_by_id(self, photo_id: str) -> Optional[Photo]:
        """Get a photo by ID."""
        return self.photo_repository.get_by_id(photo_id)
    
    def get_photos_by_pet(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[Photo]:
        """Get photos by pet ID with pagination."""
        return self.photo_repository.get_by_pet_id(pet_id, skip=skip, limit=limit)
    
    def get_primary_photo(self, pet_id: str) -> Optional[Photo]:
        """Get the primary photo for a pet."""
        return self.photo_repository.get_primary_photo(pet_id)
    
    def get_photos_by_uploader(self, uploaded_by: int, skip: int = 0, limit: int = 100) -> List[Photo]:
        """Get photos by uploader with pagination."""
        return self.photo_repository.get_by_uploaded_by(uploaded_by, skip=skip, limit=limit)
    
    def update_photo(self, photo_id: str, photo_data: PhotoUpdate) -> Optional[Photo]:
        """Update a photo with business logic validation."""
        # Check if photo exists
        existing_photo = self.photo_repository.get_by_id(photo_id)
        if not existing_photo:
            return None
        
        # Prepare update data
        update_data = {}
        if photo_data.is_primary is not None:
            update_data["is_primary"] = photo_data.is_primary
        if photo_data.is_active is not None:
            update_data["is_active"] = photo_data.is_active
        
        # Update the photo
        updated_photo = self.photo_repository.update(photo_id, **update_data)
        
        # If setting as primary, unset other primary photos
        if photo_data.is_primary:
            self.photo_repository.set_primary_photo(str(existing_photo.pet_id), photo_id)
        
        return updated_photo
    
    def delete_photo(self, photo_id: str) -> bool:
        """Delete a photo (soft delete)."""
        # Check if photo exists
        existing_photo = self.photo_repository.get_by_id(photo_id)
        if not existing_photo:
            return False
        
        # Soft delete by setting is_active to False
        self.photo_repository.update(photo_id, is_active=False)
        
        # If this was the primary photo, set another photo as primary
        if existing_photo.is_primary:
            other_photos = self.photo_repository.get_by_pet_id(str(existing_photo.pet_id), limit=1)
            if other_photos:
                self.photo_repository.set_primary_photo(str(existing_photo.pet_id), str(other_photos[0].id))
        
        return True
    
    def hard_delete_photo(self, photo_id: str) -> bool:
        """Hard delete a photo from database and storage."""
        # Check if photo exists
        existing_photo = self.photo_repository.get_by_id(photo_id)
        if not existing_photo:
            return False
        
        # Delete from storage
        try:
            self.storage_service.delete_file(existing_photo.file_path)
        except Exception:
            # Continue even if storage deletion fails
            pass
        
        # Delete from database
        return self.photo_repository.delete(photo_id)
    
    def set_primary_photo(self, pet_id: str, photo_id: str) -> bool:
        """Set a photo as primary for a pet."""
        return self.photo_repository.set_primary_photo(pet_id, photo_id)
    
    def get_photo_count_by_pet(self, pet_id: str) -> int:
        """Get photo count by pet ID."""
        return self.photo_repository.count_by_pet(pet_id)
    
    def get_photo_count_by_uploader(self, uploaded_by: int) -> int:
        """Get photo count by uploader."""
        return self.photo_repository.count_by_uploaded_by(uploaded_by)
    
    def get_download_url(self, photo_id: str, expires_in: int = 3600) -> Optional[str]:
        """Get a download URL for a photo."""
        photo = self.photo_repository.get_by_id(photo_id)
        if not photo:
            return None
        
        try:
            return self.storage_service.create_download_url(photo.file_path, expires_in)
        except Exception:
            return None
    
    def upload_file_data(self, photo_id: str, file_data: bytes) -> bool:
        """Upload file data for an existing photo record."""
        photo = self.photo_repository.get_by_id(photo_id)
        if not photo:
            return False
        
        try:
            return self.storage_service.upload_file(photo.file_path, file_data, photo.mime_type)
        except Exception:
            return False
