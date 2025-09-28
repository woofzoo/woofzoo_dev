"""
Photo controller for API layer.

This module provides the PhotoController class for handling HTTP requests
and responses related to photo operations.
"""

from typing import List, Optional

from fastapi import HTTPException, status

from app.schemas.photo import PhotoCreate, PhotoListResponse, PhotoResponse, PhotoUpdate, PhotoUploadRequest, PhotoUploadResponse
from app.services.photo import PhotoService


class PhotoController:
    """
    Photo controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to photo operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, photo_service: PhotoService) -> None:
        """Initialize the photo controller."""
        self.photo_service = photo_service
    
    def create_photo_upload_request(self, pet_id: str, upload_request: PhotoUploadRequest, uploaded_by: Optional[str] = None) -> PhotoUploadResponse:
        """Create a photo upload request."""
        try:
            photo, upload_url = self.photo_service.create_photo_upload_request(pet_id, upload_request, uploaded_by)
            return PhotoUploadResponse(
                photo=PhotoResponse.model_validate(photo),
                upload_url=upload_url,
                expires_in=3600
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create photo upload request"
            )
    
    def create_photo(self, photo_data: PhotoCreate) -> PhotoResponse:
        """Create a new photo."""
        try:
            photo = self.photo_service.create_photo(photo_data)
            return PhotoResponse.model_validate(photo)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create photo"
            )
    
    def get_photo(self, photo_id: str) -> PhotoResponse:
        """Get a photo by ID."""
        photo = self.photo_service.get_photo_by_id(photo_id)
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Photo with ID {photo_id} not found"
            )
        
        return PhotoResponse.model_validate(photo)
    
    def get_photos_by_pet(self, pet_id: str, skip: int = 0, limit: int = 100) -> PhotoListResponse:
        """Get photos by pet ID with pagination."""
        try:
            photos = self.photo_service.get_photos_by_pet(pet_id, skip=skip, limit=limit)
            total = self.photo_service.get_photo_count_by_pet(pet_id)
            
            photo_responses = [PhotoResponse.model_validate(photo) for photo in photos]
            return PhotoListResponse(photos=photo_responses, total=total)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve photos"
            )
    
    def get_primary_photo(self, pet_id: str) -> PhotoResponse:
        """Get the primary photo for a pet."""
        photo = self.photo_service.get_primary_photo(pet_id)
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No primary photo found for pet {pet_id}"
            )
        
        return PhotoResponse.model_validate(photo)
    
    def get_photos_by_uploader(self, uploaded_by: str, skip: int = 0, limit: int = 100) -> PhotoListResponse:
        """Get photos by uploader with pagination."""
        try:
            photos = self.photo_service.get_photos_by_uploader(uploaded_by, skip=skip, limit=limit)
            total = self.photo_service.get_photo_count_by_uploader(uploaded_by)
            
            photo_responses = [PhotoResponse.model_validate(photo) for photo in photos]
            return PhotoListResponse(photos=photo_responses, total=total)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve photos"
            )
    
    def update_photo(self, photo_id: str, photo_data: PhotoUpdate) -> PhotoResponse:
        """Update a photo."""
        try:
            photo = self.photo_service.update_photo(photo_id, photo_data)
            if not photo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Photo with ID {photo_id} not found"
                )
            
            return PhotoResponse.model_validate(photo)
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
                detail="Failed to update photo"
            )
    
    def delete_photo(self, photo_id: str) -> dict:
        """Delete a photo."""
        try:
            deleted = self.photo_service.delete_photo(photo_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Photo with ID {photo_id} not found"
                )
            
            return {"message": f"Photo with ID {photo_id} deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete photo"
            )
    
    def hard_delete_photo(self, photo_id: str) -> dict:
        """Hard delete a photo from database and storage."""
        try:
            deleted = self.photo_service.hard_delete_photo(photo_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Photo with ID {photo_id} not found"
                )
            
            return {"message": f"Photo with ID {photo_id} permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete photo"
            )
    
    def set_primary_photo(self, pet_id: str, photo_id: str) -> dict:
        """Set a photo as primary for a pet."""
        try:
            success = self.photo_service.set_primary_photo(pet_id, photo_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Photo with ID {photo_id} not found or does not belong to pet {pet_id}"
                )
            
            return {"message": f"Photo {photo_id} set as primary for pet {pet_id}"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to set primary photo"
            )
    
    def get_download_url(self, photo_id: str, expires_in: int = 3600) -> dict:
        """Get a download URL for a photo."""
        try:
            download_url = self.photo_service.get_download_url(photo_id, expires_in)
            if not download_url:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Photo with ID {photo_id} not found"
                )
            
            return {
                "download_url": download_url,
                "expires_in": expires_in
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate download URL"
            )
