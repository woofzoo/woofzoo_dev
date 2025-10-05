"""
Doctor Profile repository for database operations.

This module provides the DoctorProfileRepository class for doctor-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.doctor_profile import DoctorProfile
from app.repositories.base import BaseRepository


class DoctorProfileRepository(BaseRepository[DoctorProfile]):
    """
    Doctor Profile repository for doctor-specific database operations.
    
    This class extends BaseRepository to provide doctor-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the doctor profile repository."""
        super().__init__(DoctorProfile, session)
    
    def get_by_user_id(self, user_id: str) -> Optional[DoctorProfile]:
        """
        Get a doctor profile by user ID.
        
        Args:
            user_id: User's public ID
            
        Returns:
            DoctorProfile instance or None if not found
        """
        try:
            user_id_uuid = uuid.UUID(user_id)
            result = self.session.execute(
                select(DoctorProfile).where(DoctorProfile.user_id == user_id_uuid)
            )
            return result.scalar_one_or_none()
        except (ValueError, AttributeError):
            return None
    
    def get_by_license_number(self, license_number: str) -> Optional[DoctorProfile]:
        """
        Get a doctor profile by license number.
        
        Args:
            license_number: Doctor license number
            
        Returns:
            DoctorProfile instance or None if not found
        """
        result = self.session.execute(
            select(DoctorProfile).where(DoctorProfile.license_number == license_number)
        )
        return result.scalar_one_or_none()
    
    def get_active_doctors(self, skip: int = 0, limit: int = 100) -> List[DoctorProfile]:
        """
        Get all active doctors.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of DoctorProfile instances
        """
        result = self.session.execute(
            select(DoctorProfile)
            .where(DoctorProfile.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_verified_doctors(self, skip: int = 0, limit: int = 100) -> List[DoctorProfile]:
        """
        Get all verified doctors.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of DoctorProfile instances
        """
        result = self.session.execute(
            select(DoctorProfile)
            .where(DoctorProfile.is_verified == True)
            .where(DoctorProfile.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_by_specialization(self, specialization: str, skip: int = 0, limit: int = 100) -> List[DoctorProfile]:
        """
        Get doctors by specialization.
        
        Args:
            specialization: Doctor specialization
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of DoctorProfile instances
        """
        result = self.session.execute(
            select(DoctorProfile)
            .where(DoctorProfile.specialization == specialization)
            .where(DoctorProfile.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


