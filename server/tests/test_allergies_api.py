"""
Integration tests for Allergies API.
"""

import pytest
from fastapi import status


class TestAllergiesAPI:
    """Test suite for allergy endpoints."""
    
    @pytest.mark.asyncio
    async def test_owner_can_create_allergy(self, client, owner_user, pet):
        """Test that pet owners can create allergy records."""
        allergy_data = {
            "pet_id": str(pet.id),
            "allergen": "Chicken",
            "allergy_type": "food",
            "severity": "moderate",
            "symptoms": {"itching": True, "vomiting": False}
        }
        
        response = client.post(
            "/api/v1/allergies/",
            json=allergy_data,
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["allergen"] == "Chicken"
        assert data["allergy_type"] == "food"
        assert data["severity"] == "moderate"
    
    @pytest.mark.asyncio
    async def test_doctor_can_create_allergy(self, client, doctor_user, pet, doctor_profile, active_clinic_access):
        """Test that doctors can create allergy records for pets with active access."""
        allergy_data = {
            "pet_id": str(pet.id),
            "allergen": "Penicillin",
            "allergy_type": "medication",
            "severity": "severe",
            "diagnosed_by_doctor_id": str(doctor_profile.id)
        }
        
        response = client.post(
            "/api/v1/allergies/",
            json=allergy_data,
            headers={"Authorization": f"Bearer {doctor_user.token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["allergy_type"] == "medication"
        assert data["severity"] == "severe"
    
    @pytest.mark.asyncio
    async def test_get_allergies_by_pet(self, client, owner_user, pet):
        """Test getting all allergies for a pet."""
        response = client.get(
            f"/api/v1/allergies/pet/{pet.id}",
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_get_critical_allergies(self, client, owner_user, pet):
        """Test getting only critical allergies."""
        response = client.get(
            f"/api/v1/allergies/pet/{pet.id}/critical",
            headers={"Authorization": f"Bearer {owner_user.token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        # All returned allergies should be severe or life-threatening
        for allergy in data:
            assert allergy["severity"] in ["severe", "life_threatening"]

