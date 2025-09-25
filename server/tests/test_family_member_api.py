"""
Tests for family member management functionality.

This module contains tests for family member-related functionality including
API endpoints, service layer, and repository layer.
"""

import pytest
from fastapi import status

from app.schemas.family import FamilyMemberCreate, FamilyMemberUpdate


class TestFamilyMemberAPI:
    """Test cases for family member API endpoints."""
    
    def test_add_family_member_success(self, client, sample_family, sample_user, sample_family_member_data):
        """Test successful family member addition."""
        member_data = {**sample_family_member_data, "user_id": str(sample_user.public_id)}
        response = client.post("/api/family-members/", json=member_data, params={"family_id": str(sample_family.id)})
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["family_id"] == str(sample_family.id)
        assert data["user_id"] == str(sample_user.public_id)
        assert data["access_level"] == sample_family_member_data["access_level"]
        assert "id" in data
        assert "joined_at" in data
    
    def test_add_family_member_duplicate(self, client, sample_family_member, sample_family_member_data):
        """Test adding duplicate family member."""
        member_data = {**sample_family_member_data, "user_id": str(sample_family_member.user_id)}
        response = client.post("/api/family-members/", json=member_data, params={"family_id": str(sample_family_member.family_id)})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already a member" in response.json()["detail"]
    
    def test_add_family_member_invalid_data(self, client, sample_family):
        """Test family member addition with invalid data."""
        invalid_data = {"user_id": "invalid-uuid", "access_level": "INVALID_LEVEL"}
        response = client.post("/api/family-members/", json=invalid_data, params={"family_id": str(sample_family.id)})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_family_member_by_id_success(self, client, sample_family_member):
        """Test successful family member retrieval by ID."""
        response = client.get(f"/api/family-members/{sample_family_member.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_family_member.id)
        assert data["family_id"] == str(sample_family_member.family_id)
        assert data["user_id"] == str(sample_family_member.user_id)
        assert data["access_level"] == sample_family_member.access_level.value
    
    def test_get_family_member_by_id_not_found(self, client):
        """Test family member retrieval with non-existent ID."""
        response = client.get("/api/family-members/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_family_members_success(self, client, sample_family, sample_family_member):
        """Test successful retrieval of family members."""
        response = client.get(f"/api/family-members/?family_id={sample_family.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "members" in data
        assert "total" in data
        assert len(data["members"]) >= 1
        assert data["total"] >= 1
    
    def test_get_family_members_pagination(self, client, sample_family, sample_family_member):
        """Test pagination for family members."""
        response = client.get(f"/api/family-members/?family_id={sample_family.id}&skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["members"]) <= 1
    
    def test_get_user_families_success(self, client, sample_user, sample_family_member):
        """Test successful retrieval of user's families."""
        response = client.get(f"/api/family-members/user/{str(sample_user.public_id)}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "members" in data
        assert "total" in data
        assert len(data["members"]) >= 1
        assert data["total"] >= 1
    
    def test_get_user_families_pagination(self, client, sample_user, sample_family_member):
        """Test pagination for user's families."""
        response = client.get(f"/api/family-members/user/{str(sample_user.public_id)}?skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["members"]) <= 1
    
    def test_update_family_member_success(self, client, sample_family_member):
        """Test successful family member update."""
        update_data = {"access_level": "ADMIN"}
        response = client.put(f"/api/family-members/{sample_family_member.id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["access_level"] == update_data["access_level"]
    
    def test_update_family_member_not_found(self, client):
        """Test family member update with non-existent ID."""
        update_data = {"access_level": "ADMIN"}
        response = client.put("/api/family-members/123e4567-e89b-12d3-a456-426614174000", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_remove_family_member_success(self, client, sample_family_member):
        """Test successful family member removal."""
        response = client.delete(f"/api/family-members/{sample_family_member.id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_remove_family_member_not_found(self, client):
        """Test family member removal with non-existent ID."""
        response = client.delete("/api/family-members/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_remove_user_from_family_success(self, client, sample_family_member):
        """Test successful user removal from family."""
        response = client.delete(f"/api/family-members/family/{sample_family_member.family_id}/user/{sample_family_member.user_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_remove_user_from_family_not_member(self, client, sample_family, sample_user):
        """Test removing user who is not a member of the family."""
        response = client.delete(f"/api/family-members/family/{sample_family.id}/user/{str(sample_user.public_id)}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not a member" in response.json()["detail"]
