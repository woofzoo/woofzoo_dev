"""
Clinic Profile repository for database operations.

This module provides the ClinicProfileRepository class for clinic-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clinic_profile import ClinicProfile
from app.repositories.base import BaseRepository


class ClinicProfileRepository(BaseRepository[ClinicProfile]):
    """
    Clinic Profile repository for clinic-specific database operations.
    
    This class extends BaseRepository to provide clinic-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the clinic profile repository."""
        super().__init__(ClinicProfile, session)
    
    def get_by_user_id(self, user_id: str) -> Optional[ClinicProfile]:
        """
        Get a clinic profile by user ID.
        
        Args:
            user_id: User's public ID
            
        Returns:
            ClinicProfile instance or None if not found
        """
        try:
            user_id_uuid = uuid.UUID(user_id)
            result = self.session.execute(
                select(ClinicProfile).where(ClinicProfile.user_id == user_id_uuid)
            )
            return result.scalar_one_or_none()
        except (ValueError, AttributeError):
            return None
    
    def get_by_license_number(self, license_number: str) -> Optional[ClinicProfile]:
        """
        Get a clinic profile by license number.
        
        Args:
            license_number: Clinic license number
            
        Returns:
            ClinicProfile instance or None if not found
        """
        result = self.session.execute(
            select(ClinicProfile).where(ClinicProfile.license_number == license_number)
        )
        return result.scalar_one_or_none()
    
    def get_active_clinics(self, skip: int = 0, limit: int = 100) -> List[ClinicProfile]:
        """
        Get all active clinics.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of ClinicProfile instances
        """
        result = self.session.execute(
            select(ClinicProfile)
            .where(ClinicProfile.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_verified_clinics(self, skip: int = 0, limit: int = 100) -> List[ClinicProfile]:
        """
        Get all verified clinics.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of ClinicProfile instances
        """
        result = self.session.execute(
            select(ClinicProfile)
            .where(ClinicProfile.is_verified == True)
            .where(ClinicProfile.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[ClinicProfile]:
        """
        Search clinics by name.
        
        Args:
            name: Search term for clinic name
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of ClinicProfile instances
        """
        result = self.session.execute(
            select(ClinicProfile)
            .where(ClinicProfile.clinic_name.ilike(f"%{name}%"))
            .where(ClinicProfile.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


