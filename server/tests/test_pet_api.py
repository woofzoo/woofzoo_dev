"""
Tests for Pet API functionality.

This module contains tests for pet-related API endpoints.
"""

import pytest
from fastapi import status


class TestPetAPI:
    """Test cases for pet API endpoints."""
    
    def test_create_pet_success(self, authenticated_client, sample_owner, sample_pet_data):
        """Test successful pet creation."""
        # Include owner_id in the request body
        pet_data = {**sample_pet_data, "owner_id": str(sample_owner.id)}
        response = authenticated_client.post("/api/pets/", json=pet_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_pet_data["name"]
        assert data["pet_type"] == sample_pet_data["pet_type"]
        assert data["breed"] == sample_pet_data["breed"]
        assert data["age"] == sample_pet_data["age"]
        assert data["gender"] == sample_pet_data["gender"]
        assert data["weight"] == sample_pet_data["weight"]
        assert "id" in data
        assert "pet_id" in data
        assert data["pet_id"].startswith("DOG-GOLDEN_RETRIEVER-")
        assert "created_at" in data
        assert "updated_at" in data
        assert data["is_active"] is True
    
    def test_create_pet_invalid_type_breed(self, authenticated_client, sample_owner):
        """Test pet creation with invalid pet type and breed combination."""
        invalid_data = {
            "owner_id": str(sample_owner.id),
            "name": "Buddy",
            "pet_type": "DOG",
            "breed": "Invalid Breed",  # Invalid breed for DOG
            "age": 3,
            "gender": "Male",
            "weight": 25.5
        }
        
        response = authenticated_client.post("/api/pets/", json=invalid_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid" in response.json()["detail"]
    
    def test_create_pet_invalid_data(self, authenticated_client, sample_owner):
        """Test pet creation with invalid data."""
        invalid_data = {
            "owner_id": str(sample_owner.id),
            "name": "",  # Empty name
            "pet_type": "INVALID_TYPE",  # Invalid pet type
            "breed": "Golden Retriever",
            "age": -1,  # Invalid age
            "gender": "Invalid",  # Invalid gender
            "weight": -1.0  # Invalid weight
        }
        
        response = authenticated_client.post("/api/pets/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_pet_by_id_success(self, authenticated_client, sample_pet):
        """Test successful pet retrieval by ID."""
        response = authenticated_client.get(f"/api/pets/{sample_pet.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_pet.id)
        assert data["name"] == sample_pet.name
        assert data["pet_type"] == sample_pet.pet_type
        assert data["breed"] == sample_pet.breed
    
    def test_get_pet_by_id_not_found(self, authenticated_client):
        """Test pet retrieval by non-existent ID."""
        response = authenticated_client.get("/api/pets/non-existent-id")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_pet_by_pet_id_success(self, authenticated_client, sample_pet):
        """Test successful pet retrieval by pet_id."""
        response = authenticated_client.get(f"/api/pets/pet-id/{sample_pet.pet_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_pet.id)
        assert data["pet_id"] == sample_pet.pet_id
        assert data["name"] == sample_pet.name
    
    def test_get_pet_by_pet_id_not_found(self, authenticated_client):
        """Test pet retrieval by non-existent pet_id."""
        response = authenticated_client.get("/api/pets/pet-id/DOG-INVALID-000000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_pets_by_owner_success(self, authenticated_client, sample_pet, sample_owner):
        """Test successful retrieval of pets by owner."""
        response = authenticated_client.get(f"/api/pets/owner/{sample_owner.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pets" in data
        assert "total" in data
        assert len(data["pets"]) >= 1
        assert data["total"] >= 1
    
    def test_get_pets_by_owner_pagination(self, authenticated_client, sample_pet, sample_owner):
        """Test pet retrieval by owner with pagination."""
        response = authenticated_client.get(f"/api/pets/owner/{sample_owner.id}?skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["pets"]) <= 1
    
    def test_update_pet_success(self, authenticated_client, sample_pet):
        """Test successful pet update."""
        update_data = {
            "name": "Updated Buddy",
            "age": 4,
            "weight": 26.0
        }
        
        response = authenticated_client.patch(f"/api/pets/{sample_pet.id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["age"] == update_data["age"]
        assert data["weight"] == update_data["weight"]
        assert data["pet_type"] == sample_pet.pet_type  # Unchanged
        assert data["breed"] == sample_pet.breed  # Unchanged
    
    def test_update_pet_not_found(self, authenticated_client):
        """Test pet update with non-existent ID."""
        update_data = {"name": "Updated Name"}
        
        response = authenticated_client.patch("/api/pets/non-existent-id", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_delete_pet_success(self, authenticated_client, sample_pet):
        """Test successful pet deletion (soft delete)."""
        response = authenticated_client.delete(f"/api/pets/{sample_pet.id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_pet_not_found(self, authenticated_client):
        """Test pet deletion with non-existent ID."""
        response = authenticated_client.delete("/api/pets/non-existent-id")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_search_pets_success(self, authenticated_client, sample_pet):
        """Test successful pet search."""
        response = authenticated_client.get(f"/api/pets/search/?q={sample_pet.name}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pets" in data
        assert "total" in data
        assert len(data["pets"]) >= 1
    
    def test_search_pets_by_breed(self, authenticated_client, sample_pet):
        """Test pet search by breed."""
        response = authenticated_client.get(f"/api/pets/search/?q={sample_pet.breed}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["pets"]) >= 1
        assert data["pets"][0]["breed"] == sample_pet.breed
    
    def test_search_pets_no_results(self, authenticated_client):
        """Test pet search with no results."""
        response = authenticated_client.get("/api/pets/search/?q=nonexistent")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["pets"]) == 0
        assert data["total"] == 0
    
    def test_get_pets_by_type_success(self, authenticated_client, sample_pet):
        """Test successful retrieval of pets by type."""
        response = authenticated_client.get(f"/api/pets/type/{sample_pet.pet_type}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pets" in data
        assert "total" in data
        assert len(data["pets"]) >= 1
        assert all(pet["pet_type"] == sample_pet.pet_type for pet in data["pets"])
    
    def test_get_pets_by_breed_success(self, authenticated_client, sample_pet):
        """Test successful retrieval of pets by breed."""
        response = authenticated_client.get(f"/api/pets/breed/{sample_pet.breed}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pets" in data
        assert "total" in data
        assert len(data["pets"]) >= 1
        assert all(pet["breed"] == sample_pet.breed for pet in data["pets"])
