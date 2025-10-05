"""
Prescription repository for database operations.

This module provides the PrescriptionRepository class for prescription-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List
from datetime import date
import uuid

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from app.models.prescription import Prescription
from app.repositories.base import BaseRepository


class PrescriptionRepository(BaseRepository[Prescription]):
    """
    Prescription repository for prescription-specific database operations.
    
    This class extends BaseRepository to provide prescription-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the prescription repository."""
        super().__init__(Prescription, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[Prescription]:
        """
        Get all prescriptions for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Prescription instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Prescription)
                .where(Prescription.pet_id == pet_id_uuid)
                .order_by(desc(Prescription.prescribed_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_active_prescriptions(self, pet_id: str) -> List[Prescription]:
        """
        Get active prescriptions for a pet.
        
        Args:
            pet_id: Pet's ID
            
        Returns:
            List of active Prescription instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Prescription)
                .where(
                    and_(
                        Prescription.pet_id == pet_id_uuid,
                        Prescription.is_active == True
                    )
                )
                .order_by(desc(Prescription.prescribed_date))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_medical_record_id(self, medical_record_id: str) -> List[Prescription]:
        """
        Get all prescriptions for a specific medical record.
        
        Args:
            medical_record_id: Medical record's ID
            
        Returns:
            List of Prescription instances
        """
        try:
            record_id_uuid = uuid.UUID(medical_record_id)
            result = self.session.execute(
                select(Prescription)
                .where(Prescription.medical_record_id == record_id_uuid)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_medication_name(
        self, 
        pet_id: str, 
        medication_name: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Prescription]:
        """
        Get prescriptions for a pet filtered by medication name.
        
        Args:
            pet_id: Pet's ID
            medication_name: Name of medication to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Prescription instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Prescription)
                .where(
                    and_(
                        Prescription.pet_id == pet_id_uuid,
                        Prescription.medication_name.ilike(f"%{medication_name}%")
                    )
                )
                .order_by(desc(Prescription.prescribed_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_expiring_soon(self, pet_id: str, days: int = 7) -> List[Prescription]:
        """
        Get prescriptions expiring within specified days.
        
        Args:
            pet_id: Pet's ID
            days: Number of days to look ahead
            
        Returns:
            List of Prescription instances expiring soon
        """
        try:
            from datetime import timedelta
            pet_id_uuid = uuid.UUID(pet_id)
            end_date_threshold = date.today() + timedelta(days=days)
            
            result = self.session.execute(
                select(Prescription)
                .where(
                    and_(
                        Prescription.pet_id == pet_id_uuid,
                        Prescription.is_active == True,
                        Prescription.end_date.isnot(None),
                        Prescription.end_date <= end_date_threshold
                    )
                )
                .order_by(Prescription.end_date)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []


