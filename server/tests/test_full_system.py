"""
Full system test runner for WoofZoo.

This module provides comprehensive testing of the entire system
to ensure all components work together correctly.
"""

import pytest
from fastapi import status

from app.schemas.auth import UserSignup, UserLogin


class TestFullSystemWorkflow:
    """Test the complete system workflow."""
    
    def test_01_system_startup(self, client):
        """Test that the system starts up correctly."""
        # Test basic health check or root endpoint
        response = client.get("/")
        # This might be 404 if no root endpoint, but should not be 500
        assert response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def test_02_public_endpoints(self, client):
        """Test public endpoints that don't require authentication."""
        # Test pet types endpoints
        types_response = client.get("/api/pet-types/")
        assert types_response.status_code == status.HTTP_200_OK
        
        # Test breeds endpoint
        breeds_response = client.get("/api/pet-types/Dog/breeds")
        assert breeds_response.status_code == status.HTTP_200_OK
    
    def test_03_user_registration(self, client):
        """Test user registration."""
        user_data = {
            "email": "fullsystem@example.com",
            "password": "SecurePass123!",
            "first_name": "Full",
            "last_name": "System",
            "phone": "+1234567890",
            "roles": ["pet_owner"]
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        return user_data
    
    def test_04_user_login(self, client, user_data):
        """Test user login."""
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        
        result = response.json()
        assert "access_token" in result
        assert "refresh_token" in result
        
        return result["access_token"]
    
    def test_05_owner_creation(self, client, access_token):
        """Test owner creation with authentication."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        owner_data = {
            "phone": "+1234567890",
            "first_name": "Test",
            "last_name": "Owner",
            "email": "test.owner@example.com"
        }
        
        response = client.post("/api/owners/", json=owner_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        
        result = response.json()
        assert result["phone"] == owner_data["phone"]
        
        return result["id"]
    
    def test_06_pet_creation(self, client, access_token, owner_id):
        """Test pet creation with authentication."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        pet_data = {
            "name": "TestPet",
            "type": "Dog",
            "breed": "Golden Retriever",
            "gender": "MALE",
            "birth_date": "2020-01-15",
            "owner_id": owner_id
        }
        
        response = client.post("/api/pets/", json=pet_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        
        result = response.json()
        assert result["name"] == pet_data["name"]
        
        return result["id"]
    
    def test_07_family_creation(self, client, access_token, owner_id):
        """Test family creation with authentication."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        family_data = {
            "name": "Test Family",
            "description": "A test family for pets"
        }
        
        response = client.post(
            "/api/families/", 
            json=family_data, 
            headers=headers,
            params={"owner_id": owner_id}
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result = response.json()
        assert result["name"] == family_data["name"]
        
        return result["id"]
    
    def test_08_photo_creation(self, client, access_token, pet_id):
        """Test photo creation with authentication."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        photo_data = {
            "filename": "test_photo.jpg",
            "file_size": 1024000,
            "mime_type": "image/jpeg",
            "width": 1920,
            "height": 1080,
            "is_primary": False,
            "pet_id": pet_id,
            "uploaded_by": 1
        }
        
        response = client.post("/api/photos/", json=photo_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        
        result = response.json()
        assert result["filename"] == photo_data["filename"]
        
        return result["id"]
    
    def test_09_data_retrieval(self, client, access_token, owner_id, pet_id, family_id, photo_id):
        """Test retrieving all created data."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Get owner
        owner_response = client.get(f"/api/owners/{owner_id}", headers=headers)
        assert owner_response.status_code == status.HTTP_200_OK
        
        # Get pet
        pet_response = client.get(f"/api/pets/{pet_id}", headers=headers)
        assert pet_response.status_code == status.HTTP_200_OK
        
        # Get family
        family_response = client.get(f"/api/families/{family_id}", headers=headers)
        assert family_response.status_code == status.HTTP_200_OK
        
        # Get photo
        photo_response = client.get(f"/api/photos/{photo_id}", headers=headers)
        assert photo_response.status_code == status.HTTP_200_OK
    
    def test_10_relationship_queries(self, client, access_token, owner_id, pet_id):
        """Test relationship queries."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Get pets by owner
        pets_response = client.get(f"/api/pets/owner/{owner_id}", headers=headers)
        assert pets_response.status_code == status.HTTP_200_OK
        assert len(pets_response.json()["pets"]) >= 1
        
        # Get photos by pet
        photos_response = client.get(f"/api/photos/?pet_id={pet_id}", headers=headers)
        assert photos_response.status_code == status.HTTP_200_OK
        assert len(photos_response.json()["photos"]) >= 1
        
        # Get families by owner
        families_response = client.get(f"/api/families/?owner_id={owner_id}", headers=headers)
        assert families_response.status_code == status.HTTP_200_OK
        assert len(families_response.json()["families"]) >= 1
    
    def test_11_data_updates(self, client, access_token, owner_id, pet_id, family_id, photo_id):
        """Test updating data."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Update owner
        owner_update = {"first_name": "Updated"}
        owner_response = client.put(f"/api/owners/{owner_id}", json=owner_update, headers=headers)
        assert owner_response.status_code == status.HTTP_200_OK
        assert owner_response.json()["first_name"] == "Updated"
        
        # Update pet
        pet_update = {"name": "UpdatedPet"}
        pet_response = client.put(f"/api/pets/{pet_id}", json=pet_update, headers=headers)
        assert pet_response.status_code == status.HTTP_200_OK
        assert pet_response.json()["name"] == "UpdatedPet"
        
        # Update family
        family_update = {"name": "Updated Family"}
        family_response = client.put(f"/api/families/{family_id}", json=family_update, headers=headers)
        assert family_response.status_code == status.HTTP_200_OK
        assert family_response.json()["name"] == "Updated Family"
        
        # Update photo
        photo_update = {"is_primary": True}
        photo_response = client.put(f"/api/photos/{photo_id}", json=photo_update, headers=headers)
        assert photo_response.status_code == status.HTTP_200_OK
        assert photo_response.json()["is_primary"] == True
    
    def test_12_search_functionality(self, client, access_token):
        """Test search functionality."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Search pets
        search_response = client.get("/api/pets/search/?q=UpdatedPet", headers=headers)
        assert search_response.status_code == status.HTTP_200_OK
        
        # Search families
        family_search_response = client.get("/api/families/search/?q=Updated", headers=headers)
        assert family_search_response.status_code == status.HTTP_200_OK
        
        # Search breeds (public endpoint)
        breed_search_response = client.get("/api/pet-types/search/breeds?q=Golden")
        assert breed_search_response.status_code == status.HTTP_200_OK
    
    def test_13_token_refresh(self, client, user_data):
        """Test token refresh functionality."""
        # Login to get refresh token
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = client.post("/api/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        refresh_data = {"refresh_token": refresh_token}
        refresh_response = client.post("/api/auth/refresh", json=refresh_data)
        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access_token" in refresh_response.json()
    
    def test_14_user_profile(self, client, access_token):
        """Test user profile functionality."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Get current user
        me_response = client.get("/api/auth/me", headers=headers)
        assert me_response.status_code == status.HTTP_200_OK
        
        user_data = me_response.json()
        assert "email" in user_data
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "roles" in user_data
    
    def test_15_logout(self, client, access_token):
        """Test logout functionality."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        logout_response = client.post("/api/auth/logout", headers=headers)
        assert logout_response.status_code == status.HTTP_200_OK
    
    def test_16_error_handling(self, client, access_token):
        """Test error handling."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test invalid ID
        invalid_response = client.get("/api/owners/invalid-id", headers=headers)
        assert invalid_response.status_code == status.HTTP_404_NOT_FOUND
        
        # Test invalid data
        invalid_data = {"invalid": "data"}
        invalid_create_response = client.post("/api/owners/", json=invalid_data, headers=headers)
        assert invalid_create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_17_unauthorized_access(self, client):
        """Test unauthorized access protection."""
        # Try to access protected endpoints without authentication
        protected_endpoints = [
            "/api/owners/",
            "/api/pets/",
            "/api/families/",
            "/api/photos/",
            "/api/auth/me"
        ]
        
        for endpoint in protected_endpoints:
            response = client.get(endpoint)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_18_pagination(self, client, access_token):
        """Test pagination functionality."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test pagination on owners
        paginated_response = client.get("/api/owners/?skip=0&limit=10", headers=headers)
        assert paginated_response.status_code == status.HTTP_200_OK
        
        result = paginated_response.json()
        assert "owners" in result
        assert "total" in result
    
    def test_19_system_performance(self, client, access_token):
        """Test basic system performance."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test multiple quick requests
        for _ in range(5):
            response = client.get("/api/pet-types/")
            assert response.status_code == status.HTTP_200_OK
    
    def test_20_final_cleanup(self, client, access_token, owner_id, pet_id, family_id, photo_id):
        """Test cleanup operations."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Delete photo
        photo_delete_response = client.delete(f"/api/photos/{photo_id}", headers=headers)
        assert photo_delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Delete pet
        pet_delete_response = client.delete(f"/api/pets/{pet_id}", headers=headers)
        assert pet_delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Delete family
        family_delete_response = client.delete(f"/api/families/{family_id}", headers=headers)
        assert family_delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Delete owner
        owner_delete_response = client.delete(f"/api/owners/{owner_id}", headers=headers)
        assert owner_delete_response.status_code == status.HTTP_204_NO_CONTENT


class TestSystemValidation:
    """Test system validation and edge cases."""
    
    def test_database_consistency(self, client, access_token):
        """Test database consistency across operations."""
        # This would test that related data remains consistent
        # after various operations
        pass
    
    def test_concurrent_operations(self, client, access_token):
        """Test concurrent operations handling."""
        # This would test how the system handles multiple
        # simultaneous requests
        pass
    
    def test_data_integrity(self, client, access_token):
        """Test data integrity constraints."""
        # This would test foreign key constraints, unique constraints, etc.
        pass
