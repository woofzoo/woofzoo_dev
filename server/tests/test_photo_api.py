"""
Tests for photo management functionality.

This module contains tests for photo-related functionality including
API endpoints, service layer, and repository layer.
"""

import pytest
from fastapi import status

from app.schemas.photo import PhotoCreate, PhotoUpdate, PhotoUploadRequest


class TestPhotoAPI:
    """Test cases for photo API endpoints."""
    
    def test_create_photo_upload_request_success(self, client, sample_pet, sample_user, sample_photo_upload_data):
        """Test successful photo upload request creation."""
        upload_data = {**sample_photo_upload_data}
        response = client.post(
            "/api/photos/upload-request", 
            json=upload_data, 
            params={
                "pet_id": str(sample_pet.id),
                "uploaded_by": sample_user.id
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "photo" in data
        assert "upload_url" in data
        assert "expires_in" in data
        assert data["photo"]["pet_id"] == str(sample_pet.id)
        assert data["photo"]["filename"] == sample_photo_upload_data["filename"]
        assert data["photo"]["uploaded_by"] == sample_user.id
    
    def test_create_photo_upload_request_invalid_data(self, client, sample_pet, sample_user):
        """Test photo upload request with invalid data."""
        invalid_data = {
            "filename": "",
            "file_size": 0,
            "mime_type": "invalid/type"
        }
        response = client.post(
            "/api/photos/upload-request", 
            json=invalid_data, 
            params={
                "pet_id": str(sample_pet.id),
                "uploaded_by": sample_user.id
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_photo_success(self, client, sample_pet, sample_user, sample_photo_data):
        """Test successful photo creation."""
        photo_data = {**sample_photo_data, "pet_id": str(sample_pet.id), "uploaded_by": sample_user.id}
        response = client.post("/api/photos/", json=photo_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["pet_id"] == str(sample_pet.id)
        assert data["filename"] == sample_photo_data["filename"]
        assert data["uploaded_by"] == sample_user.id
        assert "id" in data
        assert "file_path" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_photo_invalid_data(self, client):
        """Test photo creation with invalid data."""
        invalid_data = {
            "pet_id": "invalid-uuid",
            "filename": "",
            "file_size": 0,
            "mime_type": "invalid/type"
        }
        response = client.post("/api/photos/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_photo_by_id_success(self, client, sample_photo):
        """Test successful photo retrieval by ID."""
        response = client.get(f"/api/photos/{sample_photo.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_photo.id)
        assert data["pet_id"] == str(sample_photo.pet_id)
        assert data["filename"] == sample_photo.filename
    
    def test_get_photo_by_id_not_found(self, client):
        """Test photo retrieval with non-existent ID."""
        response = client.get("/api/photos/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_photos_by_pet_success(self, client, sample_pet, sample_photo):
        """Test successful retrieval of photos by pet."""
        response = client.get(f"/api/photos/?pet_id={sample_pet.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "photos" in data
        assert "total" in data
        assert len(data["photos"]) >= 1
        assert data["total"] >= 1
    
    def test_get_photos_by_pet_pagination(self, client, sample_pet, sample_photo):
        """Test pagination for photos by pet."""
        response = client.get(f"/api/photos/?pet_id={sample_pet.id}&skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["photos"]) <= 1
    
    def test_get_primary_photo_success(self, client, sample_pet, sample_primary_photo):
        """Test successful retrieval of primary photo."""
        response = client.get(f"/api/photos/pet/{sample_pet.id}/primary")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pet_id"] == str(sample_pet.id)
        assert data["is_primary"] == True
    
    def test_get_primary_photo_not_found(self, client, sample_pet):
        """Test primary photo retrieval when no primary photo exists."""
        response = client.get(f"/api/photos/pet/{sample_pet.id}/primary")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "No primary photo found" in response.json()["detail"]
    
    def test_get_photos_by_uploader_success(self, client, sample_user, sample_photo):
        """Test successful retrieval of photos by uploader."""
        response = client.get(f"/api/photos/uploader/{sample_user.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "photos" in data
        assert "total" in data
        assert len(data["photos"]) >= 1
        assert data["total"] >= 1
    
    def test_get_photos_by_uploader_pagination(self, client, sample_user, sample_photo):
        """Test pagination for photos by uploader."""
        response = client.get(f"/api/photos/uploader/{sample_user.id}?skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["photos"]) <= 1
    
    def test_get_photo_download_url_success(self, client, sample_photo):
        """Test successful download URL generation."""
        response = client.get(f"/api/photos/{sample_photo.id}/download-url")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "download_url" in data
        assert "expires_in" in data
    
    def test_get_photo_download_url_not_found(self, client):
        """Test download URL generation with non-existent photo."""
        response = client.get("/api/photos/123e4567-e89b-12d3-a456-426614174000/download-url")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_update_photo_success(self, client, sample_photo):
        """Test successful photo update."""
        update_data = {"is_primary": True, "is_active": True}
        response = client.put(f"/api/photos/{sample_photo.id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_primary"] == update_data["is_primary"]
        assert data["is_active"] == update_data["is_active"]
    
    def test_update_photo_not_found(self, client):
        """Test photo update with non-existent ID."""
        update_data = {"is_primary": True}
        response = client.put("/api/photos/123e4567-e89b-12d3-a456-426614174000", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_delete_photo_success(self, client, sample_photo):
        """Test successful photo deletion."""
        response = client.delete(f"/api/photos/{sample_photo.id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_photo_not_found(self, client):
        """Test photo deletion with non-existent ID."""
        response = client.delete("/api/photos/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_hard_delete_photo_success(self, client, sample_photo):
        """Test successful hard photo deletion."""
        response = client.delete(f"/api/photos/{sample_photo.id}/permanent")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "permanently deleted" in data["message"]
    
    def test_hard_delete_photo_not_found(self, client):
        """Test hard photo deletion with non-existent ID."""
        response = client.delete("/api/photos/123e4567-e89b-12d3-a456-426614174000/permanent")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_set_primary_photo_success(self, client, sample_pet, sample_photo):
        """Test successful setting of primary photo."""
        response = client.post(f"/api/photos/pet/{sample_pet.id}/primary/{sample_photo.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "set as primary" in data["message"]
    
    def test_set_primary_photo_not_found(self, client, sample_pet):
        """Test setting primary photo with non-existent photo."""
        response = client.post(f"/api/photos/pet/{sample_pet.id}/primary/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
