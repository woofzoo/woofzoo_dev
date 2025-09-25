"""
Tests for Owner API functionality.

This module contains tests for owner-related API endpoints.
"""

import pytest
from fastapi import status


class TestOwnerAPI:
    """Test cases for owner API endpoints."""
    
    def test_create_owner_success(self, authenticated_client, sample_owner_data):
        """Test successful owner creation."""
        response = authenticated_client.post("/api/owners/", json=sample_owner_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["phone_number"] == sample_owner_data["phone_number"]
        assert data["name"] == sample_owner_data["name"]
        assert data["email"] == sample_owner_data["email"]
        assert data["address"] == sample_owner_data["address"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["is_active"] is True
    
    def test_create_owner_duplicate_phone(self, authenticated_client, sample_owner_data):
        """Test owner creation with duplicate phone number."""
        # Create first owner
        authenticated_client.post("/api/owners/", json=sample_owner_data)
        
        # Try to create second owner with same phone number
        response = authenticated_client.post("/api/owners/", json=sample_owner_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_create_owner_invalid_data(self, authenticated_client):
        """Test owner creation with invalid data."""
        invalid_data = {
            "phone_number": "invalid",  # Invalid phone number
            "name": "",  # Empty name
            "email": "invalid-email"  # Invalid email
        }
        
        response = authenticated_client.post("/api/owners/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_owner_by_id_success(self, authenticated_client, sample_owner):
        """Test successful owner retrieval by ID."""
        response = authenticated_client.get(f"/api/owners/{sample_owner.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_owner.id)
        assert data["phone_number"] == sample_owner.phone_number
        assert data["name"] == sample_owner.name
    
    def test_get_owner_by_id_not_found(self, authenticated_client):
        """Test owner retrieval by non-existent ID."""
        response = authenticated_client.get("/api/owners/non-existent-id")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_owner_by_phone_success(self, authenticated_client, sample_owner):
        """Test successful owner retrieval by phone number."""
        response = authenticated_client.get(f"/api/owners/phone/{sample_owner.phone_number}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_owner.id)
        assert data["phone_number"] == sample_owner.phone_number
        assert data["name"] == sample_owner.name
    
    def test_get_owner_by_phone_not_found(self, authenticated_client):
        """Test owner retrieval by non-existent phone number."""
        response = authenticated_client.get("/api/owners/phone/+9999999999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_all_owners_success(self, authenticated_client, sample_owner):
        """Test successful retrieval of all owners."""
        response = authenticated_client.get("/api/owners/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "owners" in data
        assert "total" in data
        assert len(data["owners"]) >= 1
        assert data["total"] >= 1
    
    def test_get_all_owners_pagination(self, authenticated_client, sample_owner):
        """Test owner retrieval with pagination."""
        response = authenticated_client.get("/api/owners/?skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["owners"]) <= 1
    
    def test_update_owner_success(self, authenticated_client, sample_owner):
        """Test successful owner update."""
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        
        response = authenticated_client.patch(f"/api/owners/{sample_owner.id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]
        assert data["phone_number"] == sample_owner.phone_number  # Unchanged
    
    def test_update_owner_not_found(self, authenticated_client):
        """Test owner update with non-existent ID."""
        update_data = {"name": "Updated Name"}
        
        response = authenticated_client.patch("/api/owners/non-existent-id", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_delete_owner_success(self, authenticated_client, sample_owner):
        """Test successful owner deletion (soft delete)."""
        response = authenticated_client.delete(f"/api/owners/{sample_owner.id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_owner_not_found(self, authenticated_client):
        """Test owner deletion with non-existent ID."""
        response = authenticated_client.delete("/api/owners/non-existent-id")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_search_owners_success(self, authenticated_client, sample_owner):
        """Test successful owner search."""
        response = authenticated_client.get(f"/api/owners/search/?q={sample_owner.name}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "owners" in data
        assert "total" in data
        assert len(data["owners"]) >= 1
    
    def test_search_owners_by_phone(self, authenticated_client, sample_owner):
        """Test owner search by phone number."""
        response = authenticated_client.get(f"/api/owners/search/?q={sample_owner.phone_number}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["owners"]) >= 1
        assert data["owners"][0]["phone_number"] == sample_owner.phone_number
    
    def test_search_owners_no_results(self, authenticated_client):
        """Test owner search with no results."""
        response = authenticated_client.get("/api/owners/search/?q=nonexistent")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["owners"]) == 0
        assert data["total"] == 0
