"""
Integration tests for Medical Records API.

Tests cover:
- Creating medical records (doctor vs owner)
- Reading medical records with access control
- Date range queries
- Emergency records
- Permission checks
"""

import pytest
from datetime import datetime, timedelta
from fastapi import status


class TestMedicalRecordsAPI:
    """Test suite for medical records endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_medical_record_as_doctor(self, client, doctor_user, pet, doctor_profile, clinic_profile, active_clinic_access):
        """Test that doctors can create medical records for pets with active access."""
        medical_record_data = {
            "pet_id": str(pet.id),
            "visit_date": datetime.utcnow().isoformat(),
            "clinic_id": str(clinic_profile.id),
            "doctor_id": str(doctor_profile.id),
            "visit_type": "routine_checkup",
            "chief_complaint": "Annual wellness check",
            "diagnosis": "Healthy",
            "treatment_plan": "Continue current care",
            "weight": 25.5,
            "temperature": 38.5,
            "is_emergency": False
        }
        
        response = client.post(
            "/api/v1/medical-records/",
            json=medical_record_data,
            headers={"Authorization": f"Bearer {doctor_user.token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["pet_id"] == str(pet.id)
        assert data["visit_type"] == "routine_checkup"
        assert data["created_by_role"] == "doctor"
    
    @pytest.mark.asyncio
    async def test_create_medical_record_without_access_fails(self, client, doctor_user, pet, doctor_profile, clinic_profile):
        """Test that doctors cannot create medical records without active clinic access."""
        medical_record_data = {
            "pet_id": str(pet.id),
            "visit_date": datetime.utcnow().isoformat(),
            "clinic_id": str(clinic_profile.id),
            "doctor_id": str(doctor_profile.id),
            "visit_type": "routine_checkup",
            "diagnosis": "Healthy"
        }
        
        response = client.post(
            "/api/v1/medical-records/",
            json=medical_record_data,
            headers={"Authorization": f"Bearer {doctor_user.token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.asyncio
    async def test_owner_can_view_medical_records(self, client, owner_user, pet, medical_record):
        """Test that pet owners can view all medical records for their pets."""
        response = client.get(
            f"/api/v1/medical-records/pet/{pet.id}",
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["records"]) > 0
        assert data["records"][0]["pet_id"] == str(pet.id)
    
    @pytest.mark.asyncio
    async def test_get_medical_records_by_date_range(self, client, owner_user, pet):
        """Test filtering medical records by date range."""
        start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        end_date = datetime.utcnow().isoformat()
        
        response = client.get(
            f"/api/v1/medical-records/pet/{pet.id}/date-range",
            params={"start_date": start_date, "end_date": end_date},
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "records" in data
    
    @pytest.mark.asyncio
    async def test_get_emergency_records(self, client, owner_user, pet):
        """Test getting only emergency medical records."""
        response = client.get(
            f"/api/v1/medical-records/pet/{pet.id}/emergency",
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # All returned records should be emergencies
        for record in data["records"]:
            assert record["is_emergency"] is True
    
    @pytest.mark.asyncio
    async def test_unauthorized_user_cannot_view_records(self, client, other_user, pet):
        """Test that unauthorized users cannot view medical records."""
        response = client.get(
            f"/api/v1/medical-records/pet/{pet.id}",
            headers={"Authorization": f"Bearer {other_user.token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.asyncio
    async def test_family_member_readonly_can_view(self, client, family_member_readonly, pet):
        """Test that read-only family members can view medical records."""
        response = client.get(
            f"/api/v1/medical-records/pet/{pet.id}",
            headers={"Authorization": f"Bearer {family_member_readonly.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    @pytest.mark.asyncio
    async def test_family_member_readonly_cannot_create(self, client, family_member_readonly, pet, clinic_profile, doctor_profile):
        """Test that read-only family members cannot create medical records."""
        medical_record_data = {
            "pet_id": str(pet.id),
            "visit_date": datetime.utcnow().isoformat(),
            "clinic_id": str(clinic_profile.id),
            "doctor_id": str(doctor_profile.id),
            "visit_type": "other",
            "diagnosis": "Home observation"
        }
        
        response = client.post(
            "/api/v1/medical-records/",
            json=medical_record_data,
            headers={"Authorization": f"Bearer {family_member_readonly.token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

