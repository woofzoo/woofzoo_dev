"""
Storage service for handling file operations with AWS S3.

This module provides the StorageService class for managing file uploads,
downloads, and operations with AWS S3.
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, Tuple
import mimetypes

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from PIL import Image
import io

from app.config import settings


class StorageService:
    """
    Storage service for handling file operations with AWS S3.
    
    This class provides methods for uploading, downloading, and managing
    files in AWS S3, including image processing and optimization.
    """
    
    def __init__(self) -> None:
        """Initialize the storage service."""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region
        )
        self.bucket_name = settings.s3_bucket_name
    
    def _generate_file_path(self, pet_id: str, filename: str) -> str:
        """Generate a unique file path for S3 storage."""
        # Create a unique filename to avoid conflicts
        file_ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        return f"pets/{pet_id}/photos/{unique_filename}"
    
    def _validate_file_type(self, mime_type: str) -> bool:
        """Validate if the file type is allowed."""
        allowed_types = settings.pet_photo_allowed_types
        return mime_type.lower() in [t.lower() for t in allowed_types]
    
    def _validate_file_size(self, file_size: int) -> bool:
        """Validate if the file size is within limits."""
        max_size_bytes = settings.pet_photo_max_size_mb * 1024 * 1024
        return file_size <= max_size_bytes
    
    def _process_image(self, image_data: bytes, mime_type: str) -> Tuple[bytes, int, int]:
        """
        Process and optimize image data.
        
        Args:
            image_data: Raw image data
            mime_type: MIME type of the image
            
        Returns:
            Tuple of (processed_image_data, width, height)
        """
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(image_data))
            
            # Get original dimensions
            width, height = image.size
            
            # Convert to RGB if necessary (for JPEG compatibility)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Resize if image is too large (max 1920x1080)
            max_width, max_height = 1920, 1080
            if width > max_width or height > max_height:
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                width, height = image.size
            
            # Convert to bytes
            output_buffer = io.BytesIO()
            
            # Determine format and quality
            if mime_type.lower() == 'image/jpeg':
                image.save(output_buffer, format='JPEG', quality=85, optimize=True)
            elif mime_type.lower() == 'image/png':
                image.save(output_buffer, format='PNG', optimize=True)
            else:
                # Default to JPEG
                image.save(output_buffer, format='JPEG', quality=85, optimize=True)
            
            processed_data = output_buffer.getvalue()
            return processed_data, width, height
            
        except Exception as e:
            # If processing fails, return original data
            raise ValueError(f"Failed to process image: {str(e)}")
    
    def create_upload_url(self, file_path: str, mime_type: str, expires_in: int = 3600) -> str:
        """
        Create a pre-signed URL for file upload.
        
        Args:
            file_path: Path where the file will be stored in S3
            mime_type: MIME type of the file
            expires_in: URL expiration time in seconds
            
        Returns:
            Pre-signed URL for upload
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path,
                    'ContentType': mime_type
                },
                ExpiresIn=expires_in
            )
            return url
        except (ClientError, NoCredentialsError) as e:
            raise ValueError(f"Failed to create upload URL: {str(e)}")
    
    def create_download_url(self, file_path: str, expires_in: int = 3600) -> str:
        """
        Create a pre-signed URL for file download.
        
        Args:
            file_path: Path of the file in S3
            expires_in: URL expiration time in seconds
            
        Returns:
            Pre-signed URL for download
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path
                },
                ExpiresIn=expires_in
            )
            return url
        except (ClientError, NoCredentialsError) as e:
            raise ValueError(f"Failed to create download URL: {str(e)}")
    
    def upload_file(self, file_path: str, file_data: bytes, mime_type: str) -> bool:
        """
        Upload a file directly to S3.
        
        Args:
            file_path: Path where the file will be stored in S3
            file_data: File data to upload
            mime_type: MIME type of the file
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            # Process image if it's an image file
            if mime_type.startswith('image/'):
                file_data, width, height = self._process_image(file_data, mime_type)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_path,
                Body=file_data,
                ContentType=mime_type
            )
            return True
        except (ClientError, NoCredentialsError) as e:
            raise ValueError(f"Failed to upload file: {str(e)}")
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from S3.
        
        Args:
            file_path: Path of the file in S3
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except (ClientError, NoCredentialsError) as e:
            raise ValueError(f"Failed to delete file: {str(e)}")
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in S3.
        
        Args:
            file_path: Path of the file in S3
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise ValueError(f"Failed to check file existence: {str(e)}")
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Get file information from S3.
        
        Args:
            file_path: Path of the file in S3
            
        Returns:
            Dictionary with file information or None if file doesn't exist
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return {
                'size': response['ContentLength'],
                'mime_type': response.get('ContentType', 'application/octet-stream'),
                'last_modified': response.get('LastModified'),
                'etag': response.get('ETag', '').strip('"')
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None
            raise ValueError(f"Failed to get file info: {str(e)}")
    
    def validate_upload_request(self, filename: str, file_size: int, mime_type: str) -> Tuple[bool, str]:
        """
        Validate an upload request.
        
        Args:
            filename: Original filename
            file_size: File size in bytes
            mime_type: MIME type of the file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate file type
        if not self._validate_file_type(mime_type):
            return False, f"File type {mime_type} is not allowed. Allowed types: {settings.pet_photo_allowed_types}"
        
        # Validate file size
        if not self._validate_file_size(file_size):
            max_size_mb = settings.pet_photo_max_size_mb
            return False, f"File size {file_size} bytes exceeds maximum allowed size of {max_size_mb}MB"
        
        # Validate filename
        if not filename or len(filename) > 255:
            return False, "Invalid filename"
        
        return True, ""
