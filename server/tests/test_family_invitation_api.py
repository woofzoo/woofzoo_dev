"""
Tests for family invitation management functionality.

This module contains tests for family invitation-related functionality including
API endpoints, service layer, and repository layer.
"""

import pytest
from fastapi import status

from app.schemas.family import FamilyInvitationCreate


class TestFamilyInvitationAPI:
    """Test cases for family invitation API endpoints."""
    
    def test_create_invitation_success(self, client, sample_family, sample_user, sample_family_invitation_data):
        """Test successful invitation creation."""
        invitation_data = {**sample_family_invitation_data}
        response = client.post(
            "/api/family-invitations/", 
            json=invitation_data, 
            params={
                "family_id": str(sample_family.id),
                "invited_by": str(sample_user.public_id)
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["family_id"] == str(sample_family.id)
        assert data["email"] == sample_family_invitation_data["email"]
        assert data["access_level"] == sample_family_invitation_data["access_level"]
        assert data["invited_by"] == str(sample_user.public_id)
        assert data["status"] == "PENDING"
        assert "id" in data
        assert "token" in data
        assert "expires_at" in data
        assert "created_at" in data
    
    def test_create_invitation_duplicate(self, client, sample_family_invitation, sample_user, sample_family_invitation_data):
        """Test creating duplicate invitation."""
        invitation_data = {**sample_family_invitation_data, "email": sample_family_invitation.email}
        response = client.post(
            "/api/family-invitations/", 
            json=invitation_data, 
            params={
                "family_id": str(sample_family_invitation.family_id),
                "invited_by": str(sample_user.public_id)
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_create_invitation_invalid_data(self, client, sample_family, sample_user):
        """Test invitation creation with invalid data."""
        invalid_data = {"email": "invalid-email", "access_level": "INVALID_LEVEL"}
        response = client.post(
            "/api/family-invitations/", 
            json=invalid_data, 
            params={
                "family_id": str(sample_family.id),
                "invited_by": str(sample_user.public_id)
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_invitation_by_id_success(self, client, sample_family_invitation):
        """Test successful invitation retrieval by ID."""
        response = client.get(f"/api/family-invitations/{sample_family_invitation.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_family_invitation.id)
        assert data["family_id"] == str(sample_family_invitation.family_id)
        assert data["email"] == sample_family_invitation.email
        assert data["status"] == sample_family_invitation.status
    
    def test_get_invitation_by_id_not_found(self, client):
        """Test invitation retrieval with non-existent ID."""
        response = client.get("/api/family-invitations/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_get_family_invitations_success(self, client, sample_family, sample_family_invitation):
        """Test successful retrieval of family invitations."""
        response = client.get(f"/api/family-invitations/?family_id={sample_family.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "invitations" in data
        assert "total" in data
        assert len(data["invitations"]) >= 1
        assert data["total"] >= 1
    
    def test_get_family_invitations_pagination(self, client, sample_family, sample_family_invitation):
        """Test pagination for family invitations."""
        response = client.get(f"/api/family-invitations/?family_id={sample_family.id}&skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["invitations"]) <= 1
    
    def test_get_user_invitations_success(self, client, sample_family_invitation):
        """Test successful retrieval of user invitations."""
        response = client.get(f"/api/family-invitations/user/{sample_family_invitation.email}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "invitations" in data
        assert "total" in data
        assert len(data["invitations"]) >= 1
        assert data["total"] >= 1
    
    def test_get_user_invitations_pagination(self, client, sample_family_invitation):
        """Test pagination for user invitations."""
        response = client.get(f"/api/family-invitations/user/{sample_family_invitation.email}?skip=0&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["invitations"]) <= 1
    
    def test_accept_invitation_success(self, client, sample_family_invitation, sample_user):
        """Test successful invitation acceptance."""
        response = client.post(
            "/api/family-invitations/accept",
            params={
                "token": sample_family_invitation.token,
                "user_id": str(sample_user.id)
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "accepted successfully" in data["message"]
    
    def test_accept_invitation_invalid_token(self, client, sample_user):
        """Test invitation acceptance with invalid token."""
        response = client.post(
            "/api/family-invitations/accept",
            params={
                "token": "invalid-token",
                "user_id": str(sample_user.id)
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid invitation token" in response.json()["detail"]
    
    def test_decline_invitation_success(self, client, sample_family_invitation):
        """Test successful invitation decline."""
        response = client.post(
            "/api/family-invitations/decline",
            params={"token": sample_family_invitation.token}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "declined successfully" in data["message"]
    
    def test_decline_invitation_invalid_token(self, client):
        """Test invitation decline with invalid token."""
        response = client.post(
            "/api/family-invitations/decline",
            params={"token": "invalid-token"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid invitation token" in response.json()["detail"]
    
    def test_cancel_invitation_success(self, client, sample_family_invitation):
        """Test successful invitation cancellation."""
        response = client.delete(f"/api/family-invitations/{sample_family_invitation.id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_cancel_invitation_not_found(self, client):
        """Test invitation cancellation with non-existent ID."""
        response = client.delete("/api/family-invitations/123e4567-e89b-12d3-a456-426614174000")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_resend_invitation_success(self, client, sample_family_invitation):
        """Test successful invitation resend."""
        response = client.post(f"/api/family-invitations/{sample_family_invitation.id}/resend")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(sample_family_invitation.id)
        assert "token" in data
        assert "expires_at" in data
    
    def test_resend_invitation_not_found(self, client):
        """Test invitation resend with non-existent ID."""
        response = client.post("/api/family-invitations/123e4567-e89b-12d3-a456-426614174000/resend")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_cleanup_expired_invitations(self, client):
        """Test cleanup of expired invitations."""
        response = client.post("/api/family-invitations/cleanup")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "Cleaned up" in data["message"]
