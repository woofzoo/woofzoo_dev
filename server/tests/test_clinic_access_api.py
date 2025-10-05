"""
Integration tests for Clinic Access API (OTP Workflow).
"""

import pytest
from fastapi import status


class TestClinicAccessAPI:
    """Test suite for OTP-based clinic access endpoints."""
    
    @pytest.mark.asyncio
    async def test_request_clinic_access_generates_otp(self, client, clinic_user, pet):
        """Test that requesting clinic access generates an OTP."""
        request_data = {
            "pet_id": str(pet.id),
            "clinic_id": str(clinic_user.clinic_profile.id),
            "purpose": "Annual checkup"
        }
        
        response = client.post(
            "/api/v1/clinic-access/request",
            json=request_data,
            headers={"Authorization": f"Bearer {clinic_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "otp_id" in data
        assert "expires_in_minutes" in data
        assert data["expires_in_minutes"] == 10
    
    @pytest.mark.asyncio
    async def test_grant_clinic_access_with_valid_otp(self, client, owner_user, pet, clinic_profile, doctor_profile, valid_otp):
        """Test granting clinic access with valid OTP."""
        grant_data = {
            "pet_id": str(pet.id),
            "clinic_id": str(clinic_profile.id),
            "otp_code": valid_otp.otp_code,
            "doctor_id": str(doctor_profile.id),
            "access_duration_hours": 24
        }
        
        response = client.post(
            "/api/v1/clinic-access/grant",
            json=grant_data,
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["pet_id"] == str(pet.id)
        assert data["clinic_id"] == str(clinic_profile.id)
        assert data["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_grant_clinic_access_with_invalid_otp_fails(self, client, owner_user, pet, clinic_profile, doctor_profile):
        """Test that invalid OTP fails access grant."""
        grant_data = {
            "pet_id": str(pet.id),
            "clinic_id": str(clinic_profile.id),
            "otp_code": "999999",  # Invalid OTP
            "doctor_id": str(doctor_profile.id),
            "access_duration_hours": 24
        }
        
        response = client.post(
            "/api/v1/clinic-access/grant",
            json=grant_data,
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @pytest.mark.asyncio
    async def test_non_owner_cannot_grant_access(self, client, other_user, pet, clinic_profile, doctor_profile, valid_otp):
        """Test that non-owners cannot grant clinic access."""
        grant_data = {
            "pet_id": str(pet.id),
            "clinic_id": str(clinic_profile.id),
            "otp_code": valid_otp.otp_code,
            "doctor_id": str(doctor_profile.id),
            "access_duration_hours": 24
        }
        
        response = client.post(
            "/api/v1/clinic-access/grant",
            json=grant_data,
            headers={"Authorization": f"Bearer {other_user.token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.asyncio
    async def test_revoke_clinic_access(self, client, owner_user, active_clinic_access):
        """Test revoking clinic access."""
        revoke_data = {
            "access_id": str(active_clinic_access.id)
        }
        
        response = client.post(
            "/api/v1/clinic-access/revoke",
            json=revoke_data,
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Access revoked successfully"
    
    @pytest.mark.asyncio
    async def test_non_owner_cannot_revoke_access(self, client, other_user, active_clinic_access):
        """Test that non-owners cannot revoke clinic access."""
        revoke_data = {
            "access_id": str(active_clinic_access.id)
        }
        
        response = client.post(
            "/api/v1/clinic-access/revoke",
            json=revoke_data,
            headers={"Authorization": f"Bearer {other_user.token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

