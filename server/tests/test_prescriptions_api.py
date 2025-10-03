"""
Integration tests for Prescriptions API.
"""

import pytest
from datetime import date, timedelta
from fastapi import status


class TestPrescriptionsAPI:
    """Test suite for prescription endpoints."""
    
    @pytest.mark.asyncio
    async def test_doctor_can_create_prescription(self, client, doctor_user, pet, doctor_profile, medical_record):
        """Test that doctors can create prescriptions."""
        prescription_data = {
            "medical_record_id": str(medical_record.id),
            "pet_id": str(pet.id),
            "medication_name": "Amoxicillin",
            "dosage": "250",
            "dosage_unit": "mg",
            "frequency": "Twice daily",
            "route": "Oral",
            "duration": "10 days",
            "prescribed_by_doctor_id": str(doctor_profile.id),
            "prescribed_date": date.today().isoformat(),
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=10)).isoformat(),
            "quantity": 20.0,
            "refills_allowed": 0
        }
        
        response = client.post(
            "/api/v1/prescriptions/",
            json=prescription_data,
            headers={"Authorization": f"Bearer {doctor_user.token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["medication_name"] == "Amoxicillin"
        assert data["dosage"] == "250"
    
    @pytest.mark.asyncio
    async def test_owner_cannot_create_prescription(self, client, owner_user, pet, medical_record, doctor_profile):
        """Test that pet owners cannot create professional prescriptions."""
        prescription_data = {
            "medical_record_id": str(medical_record.id),
            "pet_id": str(pet.id),
            "medication_name": "Test Med",
            "dosage": "10",
            "dosage_unit": "mg",
            "frequency": "Daily",
            "route": "Oral",
            "duration": "7 days",
            "prescribed_by_doctor_id": str(doctor_profile.id),
            "prescribed_date": date.today().isoformat(),
            "start_date": date.today().isoformat(),
            "quantity": 7.0,
            "refills_allowed": 0
        }
        
        response = client.post(
            "/api/v1/prescriptions/",
            json=prescription_data,
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.asyncio
    async def test_get_prescriptions_by_pet(self, client, owner_user, pet):
        """Test getting all prescriptions for a pet."""
        response = client.get(
            f"/api/v1/prescriptions/pet/{pet.id}",
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_update_prescription(self, client, doctor_user, prescription):
        """Test updating a prescription."""
        update_data = {
            "is_active": False
        }
        
        response = client.put(
            f"/api/v1/prescriptions/{prescription.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {doctor_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] is False

