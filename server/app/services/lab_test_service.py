"""
Lab Test Service for business logic operations.

This module provides the LabTestService class for lab test-related
business logic with access control.
"""

from typing import List, Optional
import uuid

from app.models.lab_test import LabTest
from app.models.user import User
from app.repositories.lab_test import LabTestRepository
from app.schemas.lab_test import LabTestCreate, LabTestUpdate
from app.services.permission_service import PermissionService


class LabTestService:
    """
    Lab Test service for business logic operations.
    
    This class handles business logic for lab test operations,
    including validation, access control, and coordination.
    """
    
    def __init__(
        self,
        lab_test_repository: LabTestRepository,
        permission_service: PermissionService
    ):
        """Initialize the lab test service."""
        self.lab_test_repository = lab_test_repository
        self.permission_service = permission_service
    
    def create_lab_test(
        self,
        lab_test_data: LabTestCreate,
        current_user: User
    ) -> Optional[LabTest]:
        """
        Create/order a new lab test with access control.
        
        Args:
            lab_test_data: Lab test data
            current_user: User ordering the test
            
        Returns:
            Created LabTest or None if unauthorized
        """
        # Only doctors can order lab tests
        if not self.permission_service.can_order_lab_tests(
            current_user,
            lab_test_data.pet_id
        ):
            raise PermissionError("Only doctors can order lab tests")
        
        # Convert UUID strings
        try:
            pet_id_uuid = uuid.UUID(lab_test_data.pet_id)
            doctor_id_uuid = uuid.UUID(lab_test_data.ordered_by_doctor_id)
            medical_record_id_uuid = uuid.UUID(lab_test_data.medical_record_id) if lab_test_data.medical_record_id else None
            clinic_id_uuid = uuid.UUID(lab_test_data.performed_by_clinic_id) if lab_test_data.performed_by_clinic_id else None
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        # Create the lab test
        lab_test = self.lab_test_repository.create(
            pet_id=pet_id_uuid,
            medical_record_id=medical_record_id_uuid,
            test_name=lab_test_data.test_name,
            test_type=lab_test_data.test_type,
            ordered_by_doctor_id=doctor_id_uuid,
            ordered_at=lab_test_data.ordered_at,
            performed_at=lab_test_data.performed_at,
            performed_by_clinic_id=clinic_id_uuid,
            status=lab_test_data.status,
            results=lab_test_data.results,
            results_json=lab_test_data.results_json or {},
            results_file_url=lab_test_data.results_file_url,
            reference_ranges=lab_test_data.reference_ranges or {},
            abnormal_flags=lab_test_data.abnormal_flags or {},
            interpretation=lab_test_data.interpretation,
            is_abnormal=lab_test_data.is_abnormal
        )
        
        return lab_test
    
    def get_lab_test(
        self,
        lab_test_id: str,
        current_user: User
    ) -> Optional[LabTest]:
        """Get a lab test by ID with access control."""
        lab_test = self.lab_test_repository.get_by_id(lab_test_id)
        
        if not lab_test:
            return None
        
        if not self.permission_service.can_read_lab_tests(
            current_user,
            str(lab_test.pet_id)
        ):
            raise PermissionError("You don't have permission to view this lab test")
        
        return lab_test
    
    def get_lab_tests_by_pet(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[LabTest]:
        """Get all lab tests for a pet with access control."""
        if not self.permission_service.can_read_lab_tests(current_user, pet_id):
            raise PermissionError("You don't have permission to view lab tests for this pet")
        
        return self.lab_test_repository.get_by_pet_id(pet_id, skip=skip, limit=limit)
    
    def get_abnormal_results(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[LabTest]:
        """Get lab tests with abnormal results for a pet."""
        if not self.permission_service.can_read_lab_tests(current_user, pet_id):
            raise PermissionError("You don't have permission to view lab tests for this pet")
        
        return self.lab_test_repository.get_abnormal_results(pet_id, skip=skip, limit=limit)
    
    def update_lab_test(
        self,
        lab_test_id: str,
        lab_test_data: LabTestUpdate,
        current_user: User
    ) -> Optional[LabTest]:
        """Update a lab test (e.g., add results)."""
        existing = self.lab_test_repository.get_by_id(lab_test_id)
        
        if not existing:
            return None
        
        # Only doctors can update lab tests
        if not self.permission_service.can_order_lab_tests(
            current_user,
            str(existing.pet_id)
        ):
            raise PermissionError("Only doctors can update lab tests")
        
        # Prepare update data
        update_data = {}
        if lab_test_data.performed_at is not None:
            update_data["performed_at"] = lab_test_data.performed_at
        if lab_test_data.status is not None:
            update_data["status"] = lab_test_data.status
        if lab_test_data.results is not None:
            update_data["results"] = lab_test_data.results
        if lab_test_data.results_json is not None:
            update_data["results_json"] = lab_test_data.results_json
        if lab_test_data.results_file_url is not None:
            update_data["results_file_url"] = lab_test_data.results_file_url
        if lab_test_data.abnormal_flags is not None:
            update_data["abnormal_flags"] = lab_test_data.abnormal_flags
        if lab_test_data.interpretation is not None:
            update_data["interpretation"] = lab_test_data.interpretation
        if lab_test_data.is_abnormal is not None:
            update_data["is_abnormal"] = lab_test_data.is_abnormal
        
        return self.lab_test_repository.update(lab_test_id, **update_data)

