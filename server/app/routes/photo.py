"""
Photo routes for API endpoints.

This module defines all photo-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query, status

from app.controllers.photo import PhotoController
from app.dependencies import get_photo_controller, get_current_user_id
from app.schemas.photo import PhotoCreate, PhotoListResponse, PhotoResponse, PhotoUpdate, PhotoUploadRequest, PhotoUploadResponse

# Create router
router = APIRouter(prefix="/photos", tags=["photos"])


# API Endpoints
@router.post(
    "/upload-request",
    response_model=PhotoUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create photo upload request",
    description="Create a photo record and generate pre-signed upload URL"
)
def create_photo_upload_request(
    pet_id: str = Query(..., description="Pet's unique identifier"),
    uploaded_by: str = Query(None, description="Uploader user's public_id (UUID)"),
    upload_request: PhotoUploadRequest = None,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> PhotoUploadResponse:
    """Create a photo upload request with pre-signed URL."""
    return controller.create_photo_upload_request(pet_id, upload_request, uploaded_by)


@router.post(
    "/",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new photo",
    description="Create a new photo with the provided data"
)
def create_photo(
    photo_data: PhotoCreate,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> PhotoResponse:
    """Create a new photo."""
    return controller.create_photo(photo_data)


@router.get(
    "/",
    response_model=PhotoListResponse,
    summary="Get photos by pet",
    description="Retrieve photos for a specific pet with optional pagination"
)
def get_photos_by_pet(
    pet_id: str = Query(..., description="Pet's unique identifier"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> PhotoListResponse:
    """Get photos by pet ID with pagination."""
    return controller.get_photos_by_pet(pet_id, skip=skip, limit=limit)


@router.get(
    "/pet/{pet_id}/primary",
    response_model=PhotoResponse,
    summary="Get primary photo for pet",
    description="Retrieve the primary photo for a specific pet"
)
def get_primary_photo(
    pet_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> PhotoResponse:
    """Get the primary photo for a pet."""
    return controller.get_primary_photo(pet_id)


@router.get(
    "/uploader/{uploaded_by}",
    response_model=PhotoListResponse,
    summary="Get photos by uploader",
    description="Retrieve photos uploaded by a specific user with optional pagination"
)
def get_photos_by_uploader(
    uploaded_by: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> PhotoListResponse:
    """Get photos by uploader with pagination."""
    return controller.get_photos_by_uploader(uploaded_by, skip=skip, limit=limit)


@router.get(
    "/{photo_id}",
    response_model=PhotoResponse,
    summary="Get a photo by ID",
    description="Retrieve a specific photo by its ID"
)
def get_photo(
    photo_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> PhotoResponse:
    """Get a photo by ID."""
    return controller.get_photo(photo_id)


@router.get(
    "/{photo_id}/download-url",
    summary="Get photo download URL",
    description="Generate a pre-signed download URL for a photo"
)
def get_photo_download_url(
    photo_id: str,
    expires_in: int = Query(default=3600, ge=300, le=86400, description="URL expiration time in seconds"),
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> dict:
    """Get a download URL for a photo."""
    return controller.get_download_url(photo_id, expires_in)


@router.put(
    "/{photo_id}",
    response_model=PhotoResponse,
    summary="Update a photo",
    description="Update an existing photo with the provided data"
)
def update_photo(
    photo_id: str,
    photo_data: PhotoUpdate,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> PhotoResponse:
    """Update a photo."""
    return controller.update_photo(photo_id, photo_data)


@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a photo",
    description="Soft delete a photo by its ID"
)
def delete_photo(
    photo_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> None:
    """Delete a photo (soft delete)."""
    controller.delete_photo(photo_id)


@router.delete(
    "/{photo_id}/permanent",
    summary="Permanently delete a photo",
    description="Hard delete a photo from database and storage"
)
def hard_delete_photo(
    photo_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> dict:
    """Permanently delete a photo."""
    return controller.hard_delete_photo(photo_id)


@router.post(
    "/pet/{pet_id}/primary/{photo_id}",
    summary="Set primary photo",
    description="Set a photo as the primary photo for a pet"
)
def set_primary_photo(
    pet_id: str,
    photo_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: PhotoController = Depends(get_photo_controller)
) -> dict:
    """Set a photo as primary for a pet."""
    return controller.set_primary_photo(pet_id, photo_id)
