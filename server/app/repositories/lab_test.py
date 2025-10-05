"""
Lab Test repository for database operations.

This module provides the LabTestRepository class for lab test-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List
import uuid

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from app.models.lab_test import LabTest, TestStatus
from app.repositories.base import BaseRepository


class LabTestRepository(BaseRepository[LabTest]):
    """
    Lab Test repository for lab test-specific database operations.
    
    This class extends BaseRepository to provide lab test-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the lab test repository."""
        super().__init__(LabTest, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[LabTest]:
        """
        Get all lab tests for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of LabTest instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(LabTest)
                .where(LabTest.pet_id == pet_id_uuid)
                .order_by(desc(LabTest.ordered_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_medical_record_id(self, medical_record_id: str) -> List[LabTest]:
        """
        Get all lab tests for a specific medical record.
        
        Args:
            medical_record_id: Medical record's ID
            
        Returns:
            List of LabTest instances
        """
        try:
            record_id_uuid = uuid.UUID(medical_record_id)
            result = self.session.execute(
                select(LabTest)
                .where(LabTest.medical_record_id == record_id_uuid)
                .order_by(desc(LabTest.ordered_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_status(self, pet_id: str, status: TestStatus) -> List[LabTest]:
        """
        Get lab tests for a pet filtered by status.
        
        Args:
            pet_id: Pet's ID
            status: Test status to filter by
            
        Returns:
            List of LabTest instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(LabTest)
                .where(
                    and_(
                        LabTest.pet_id == pet_id_uuid,
                        LabTest.status == status
                    )
                )
                .order_by(desc(LabTest.ordered_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_abnormal_results(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[LabTest]:
        """
        Get lab tests with abnormal results for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of LabTest instances with abnormal results
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(LabTest)
                .where(
                    and_(
                        LabTest.pet_id == pet_id_uuid,
                        LabTest.is_abnormal == True,
                        LabTest.status == TestStatus.COMPLETED
                    )
                )
                .order_by(desc(LabTest.ordered_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_pending_tests(self, clinic_id: str, skip: int = 0, limit: int = 100) -> List[LabTest]:
        """
        Get pending lab tests for a clinic.
        
        Args:
            clinic_id: Clinic's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pending LabTest instances
        """
        try:
            clinic_id_uuid = uuid.UUID(clinic_id)
            result = self.session.execute(
                select(LabTest)
                .where(
                    and_(
                        LabTest.performed_by_clinic_id == clinic_id_uuid,
                        LabTest.status.in_([TestStatus.ORDERED, TestStatus.IN_PROGRESS])
                    )
                )
                .order_by(LabTest.ordered_at)
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_test_type(self, pet_id: str, test_type: str, skip: int = 0, limit: int = 100) -> List[LabTest]:
        """
        Get lab tests for a pet filtered by test type.
        
        Args:
            pet_id: Pet's ID
            test_type: Type of test to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of LabTest instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(LabTest)
                .where(
                    and_(
                        LabTest.pet_id == pet_id_uuid,
                        LabTest.test_type == test_type
                    )
                )
                .order_by(desc(LabTest.ordered_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []


