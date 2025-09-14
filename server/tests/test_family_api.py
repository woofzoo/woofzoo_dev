"""
Tests for family management functionality.

This module contains tests for family-related functionality including
API endpoints, service layer, and repository layer.
"""

import pytest
from fastapi import status

from app.schemas.family import FamilyCreate, FamilyUpdate


class TestFamilyAPI:
    """Test cases for family API endpoints."""
    
    def test_create_family_success(self, client, sample_owner, sample_family_data):
        """Test successful family creation."""
        family_data = {**sample_family_data, "owner_id": str(sample_owner.id)}
        response = client.post("/api/families/", json=family_data, params={"owner_id": str(sample_owner.id)})
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_family_data["name"]
        assert data["description"] == sample_family_data["description"]
        assert data["owner_id"] == str(sample_owner.id)
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_family_invalid_data(self, client, sample_owner):
        """Test family creation with invalid data."""
        invalid_data = {"name": "", "description": "A" * 501}  # Empty name, too long description
        response = client.post("/api/families/", json=invalid_data, params={"owner_id": str(sample_owner.id)})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_family_by_id_success(self, client, sample_family):
        """Test successful family retrieval by ID."""
        response = client.get(f"/api/families/{sample_family.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_family.id)
        assert data["name"] == sample_family.name
        assert data["description"] == sample_family.description
    
    def test_get_family_by_id_not_found(self, client):
        """Test family retrieval with non-existent ID."""
        response = client.get("/api/families/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_families_by_owner_success(self, client, sample_owner, sample_family):
        """Test successful retrieval of families by owner."""
        response = client.get(f"/api/families/?owner_id={sample_owner.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "families" in data
        assert "total" in data
        assert len(data["families"]) >= 1
        assert data["total"] >= 1
    
    def test_get_families_by_owner_pagination(self, client, sample_owner, sample_family):
        """Test pagination for families by owner."""
        response = client.get(f"/api/families/?owner_id={sample_owner.id}&skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["families"]) <= 1
    
    def test_update_family_success(self, client, sample_family):
        """Test successful family update."""
        update_data = {"name": "Updated Family Name", "description": "Updated description"}
        response = client.put(f"/api/families/{sample_family.id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
    
    def test_update_family_not_found(self, client):
        """Test family update with non-existent ID."""
        update_data = {"name": "Updated Name"}
        response = client.put("/api/families/123e4567-e89b-12d3-a456-426614174000", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_delete_family_success(self, client, sample_family):
        """Test successful family deletion."""
        response = client.delete(f"/api/families/{sample_family.id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_family_not_found(self, client):
        """Test family deletion with non-existent ID."""
        response = client.delete("/api/families/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_search_families_success(self, client, sample_family):
        """Test successful family search."""
        response = client.get(f"/api/families/search/?q={sample_family.name}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "families" in data
        assert "total" in data
        assert len(data["families"]) >= 1
    
    def test_search_families_with_owner_filter(self, client, sample_owner, sample_family):
        """Test family search with owner filter."""
        response = client.get(f"/api/families/search/?q={sample_family.name}&owner_id={sample_owner.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "families" in data
        assert "total" in data
    
    def test_search_families_no_results(self, client):
        """Test family search with no results."""
        response = client.get("/api/families/search/?q=nonexistentfamily")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["families"] == []
        assert data["total"] == 0
