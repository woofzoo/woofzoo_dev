"""
Tests for Pet Types API functionality.

This module contains tests for pet types and breeds related API endpoints.
"""

import pytest
from fastapi import status


class TestPetTypesAPI:
    """Test cases for pet types API endpoints."""
    
    def test_get_pet_types_success(self, client):
        """Test successful retrieval of all pet types."""
        response = client.get("/api/pet-types/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "types" in data
        assert len(data["types"]) > 0
        assert "DOG" in data["types"]
        assert "CAT" in data["types"]
        assert "BIRD" in data["types"]
    
    def test_get_breeds_for_type_success(self, client):
        """Test successful retrieval of breeds for a pet type."""
        response = client.get("/api/pet-types/DOG/breeds")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pet_type" in data
        assert "breeds" in data
        assert data["pet_type"] == "DOG"
        assert len(data["breeds"]) > 0
        assert "Golden Retriever" in data["breeds"]
        assert "Labrador Retriever" in data["breeds"]
    
    def test_get_breeds_for_invalid_type(self, client):
        """Test retrieval of breeds for an invalid pet type."""
        response = client.get("/api/pet-types/INVALID_TYPE/breeds")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "No breeds found" in response.json()["detail"]
    
    def test_get_pet_type_info_success(self, client):
        """Test successful retrieval of pet type information."""
        response = client.get("/api/pet-types/DOG/info")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pet_type" in data
        assert "breeds" in data
        assert "breed_count" in data
        assert data["pet_type"] == "DOG"
        assert len(data["breeds"]) > 0
        assert data["breed_count"] == len(data["breeds"])
    
    def test_get_pet_type_info_invalid_type(self, client):
        """Test retrieval of pet type information for invalid type."""
        response = client.get("/api/pet-types/INVALID_TYPE/info")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_validate_pet_type_and_breed_valid(self, client):
        """Test validation of valid pet type and breed combination."""
        response = client.get("/api/pet-types/validate/DOG/Golden Retriever")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pet_type" in data
        assert "breed" in data
        assert "is_valid" in data
        assert data["pet_type"] == "DOG"
        assert data["breed"] == "Golden Retriever"
        assert data["is_valid"] is True
    
    def test_validate_pet_type_and_breed_invalid(self, client):
        """Test validation of invalid pet type and breed combination."""
        response = client.get("/api/pet-types/validate/DOG/Invalid Breed")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pet_type" in data
        assert "breed" in data
        assert "is_valid" in data
        assert data["pet_type"] == "DOG"
        assert data["breed"] == "Invalid Breed"
        assert data["is_valid"] is False
    
    def test_search_breeds_success(self, client):
        """Test successful breed search."""
        response = client.get("/api/pet-types/search/breeds?q=Golden")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "search_term" in data
        assert "pet_type" in data
        assert "breeds" in data
        assert "count" in data
        assert data["search_term"] == "Golden"
        assert data["pet_type"] is None
        assert len(data["breeds"]) > 0
        assert data["count"] == len(data["breeds"])
        assert any("Golden" in breed for breed in data["breeds"])
    
    def test_search_breeds_with_pet_type_filter(self, client):
        """Test breed search with pet type filter."""
        response = client.get("/api/pet-types/search/breeds?q=Golden&pet_type=DOG")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "search_term" in data
        assert "pet_type" in data
        assert "breeds" in data
        assert "count" in data
        assert data["search_term"] == "Golden"
        assert data["pet_type"] == "DOG"
        assert len(data["breeds"]) > 0
        assert data["count"] == len(data["breeds"])
        assert all("Golden" in breed for breed in data["breeds"])
    
    def test_search_breeds_no_results(self, client):
        """Test breed search with no results."""
        response = client.get("/api/pet-types/search/breeds?q=nonexistent")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "search_term" in data
        assert "breeds" in data
        assert "count" in data
        assert data["search_term"] == "nonexistent"
        assert len(data["breeds"]) == 0
        assert data["count"] == 0
    
    def test_search_breeds_empty_query(self, client):
        """Test breed search with empty query."""
        response = client.get("/api/pet-types/search/breeds?q=")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_breeds_for_cat_type(self, client):
        """Test retrieval of breeds for CAT type."""
        response = client.get("/api/pet-types/CAT/breeds")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pet_type"] == "CAT"
        assert len(data["breeds"]) > 0
        assert "Persian" in data["breeds"]
        assert "Maine Coon" in data["breeds"]
    
    def test_get_breeds_for_bird_type(self, client):
        """Test retrieval of breeds for BIRD type."""
        response = client.get("/api/pet-types/BIRD/breeds")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pet_type"] == "BIRD"
        assert len(data["breeds"]) > 0
        assert "Parrot" in data["breeds"]
        assert "Cockatiel" in data["breeds"]
    
    def test_validate_cat_breed(self, client):
        """Test validation of valid cat breed."""
        response = client.get("/api/pet-types/validate/CAT/Persian")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pet_type"] == "CAT"
        assert data["breed"] == "Persian"
        assert data["is_valid"] is True
    
    def test_validate_invalid_combination(self, client):
        """Test validation of invalid pet type and breed combination."""
        response = client.get("/api/pet-types/validate/CAT/Golden Retriever")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pet_type"] == "CAT"
        assert data["breed"] == "Golden Retriever"
        assert data["is_valid"] is False
