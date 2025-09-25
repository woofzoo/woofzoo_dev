"""
Photo Pydantic schemas for request/response validation.

This module defines Pydantic models for photo-related API operations.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class PhotoBase(BaseModel):
    """Base Photo schema with common fields."""
    
    filename: str = Field(..., min_length=1, max_length=255, description="Original filename")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    mime_type: str = Field(..., min_length=1, max_length=100, description="MIME type of the file")
    width: Optional[int] = Field(None, gt=0, description="Image width in pixels")
    height: Optional[int] = Field(None, gt=0, description="Image height in pixels")
    is_primary: bool = Field(default=False, description="Whether this is the primary photo")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "pet_photo.jpg",
                "file_size": 1024000,
                "mime_type": "image/jpeg",
                "width": 1920,
                "height": 1080,
                "is_primary": False
            }
        }
    )


class PhotoCreate(PhotoBase):
    """Schema for creating a new photo."""
    
    pet_id: str = Field(..., description="Pet's unique identifier (UUID)")
    uploaded_by: Optional[str] = Field(None, description="Uploader user's public_id (UUID)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "pet_photo.jpg",
                "file_size": 1024000,
                "mime_type": "image/jpeg",
                "width": 1920,
                "height": 1080,
                "is_primary": False,
                "uploaded_by": "123e4567-e89b-12d3-a456-426614174009"
            }
        }
    )


class PhotoUpdate(BaseModel):
    """Schema for updating an existing photo."""
    
    is_primary: Optional[bool] = Field(None, description="Whether this is the primary photo")
    is_active: Optional[bool] = Field(None, description="Whether the photo is active/visible")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "is_primary": True,
                "is_active": True
            }
        }
    )


class PhotoResponse(PhotoBase):
    """Schema for photo response."""
    
    id: str = Field(..., description="Photo unique identifier")
    pet_id: str = Field(..., description="Pet's unique identifier")
    file_path: str = Field(..., description="Path in cloud storage")
    is_active: bool = Field(..., description="Whether the photo is active/visible")
    uploaded_by: Optional[str] = Field(None, description="Uploader user's public_id (UUID)")
    created_at: datetime = Field(..., description="Photo creation timestamp")
    updated_at: datetime = Field(..., description="Photo last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "pet_id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "pet_photo.jpg",
                "file_path": "pets/123e4567-e89b-12d3-a456-426614174000/photos/pet_photo.jpg",
                "file_size": 1024000,
                "mime_type": "image/jpeg",
                "width": 1920,
                "height": 1080,
                "is_primary": False,
                "is_active": True,
                "uploaded_by": "123e4567-e89b-12d3-a456-426614174009",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
    )


class PhotoUploadResponse(BaseModel):
    """Schema for photo upload response."""
    
    photo: PhotoResponse = Field(..., description="Uploaded photo information")
    upload_url: str = Field(..., description="Pre-signed URL for uploading the file")
    expires_in: int = Field(..., description="URL expiration time in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "photo": {
                    "id": "123e4567-e89b-12d3-a456-426614174002",
                    "pet_id": "123e4567-e89b-12d3-a456-426614174000",
                    "filename": "pet_photo.jpg",
                    "file_path": "pets/123e4567-e89b-12d3-a456-426614174000/photos/pet_photo.jpg",
                    "file_size": 1024000,
                    "mime_type": "image/jpeg",
                    "width": 1920,
                    "height": 1080,
                    "is_primary": False,
                    "is_active": True,
                    "uploaded_by": "123e4567-e89b-12d3-a456-426614174009",
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                },
                "upload_url": "https://s3.amazonaws.com/bucket/presigned-url",
                "expires_in": 3600
            }
        }
    )


class PhotoListResponse(BaseModel):
    """Schema for list of photos response."""
    
    photos: List[PhotoResponse] = Field(..., description="List of photos")
    total: int = Field(..., description="Total number of photos")


class PhotoUploadRequest(BaseModel):
    """Schema for photo upload request."""
    
    filename: str = Field(..., min_length=1, max_length=255, description="Original filename")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    mime_type: str = Field(..., min_length=1, max_length=100, description="MIME type of the file")
    is_primary: bool = Field(default=False, description="Whether this is the primary photo")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "pet_photo.jpg",
                "file_size": 1024000,
                "mime_type": "image/jpeg",
                "is_primary": False
            }
        }
    )
