"""
Allergy repository for database operations.

This module provides the AllergyRepository class for allergy-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List
import uuid

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from app.models.allergy import Allergy, AllergyType, AllergySeverity
from app.repositories.base import BaseRepository


class AllergyRepository(BaseRepository[Allergy]):
    """
    Allergy repository for allergy-specific database operations.
    
    This class extends BaseRepository to provide allergy-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the allergy repository."""
        super().__init__(Allergy, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[Allergy]:
        """
        Get all allergies for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Allergy instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Allergy)
                .where(Allergy.pet_id == pet_id_uuid)
                .order_by(desc(Allergy.created_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_active_allergies(self, pet_id: str) -> List[Allergy]:
        """
        Get active allergies for a pet.
        
        Args:
            pet_id: Pet's ID
            
        Returns:
            List of active Allergy instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Allergy)
                .where(
                    and_(
                        Allergy.pet_id == pet_id_uuid,
                        Allergy.is_active == True
                    )
                )
                .order_by(desc(Allergy.severity))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_allergy_type(self, pet_id: str, allergy_type: AllergyType) -> List[Allergy]:
        """
        Get allergies for a pet filtered by type.
        
        Args:
            pet_id: Pet's ID
            allergy_type: Type of allergy to filter by
            
        Returns:
            List of Allergy instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Allergy)
                .where(
                    and_(
                        Allergy.pet_id == pet_id_uuid,
                        Allergy.allergy_type == allergy_type,
                        Allergy.is_active == True
                    )
                )
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_severity(self, pet_id: str, severity: AllergySeverity) -> List[Allergy]:
        """
        Get allergies for a pet filtered by severity.
        
        Args:
            pet_id: Pet's ID
            severity: Severity level to filter by
            
        Returns:
            List of Allergy instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Allergy)
                .where(
                    and_(
                        Allergy.pet_id == pet_id_uuid,
                        Allergy.severity == severity,
                        Allergy.is_active == True
                    )
                )
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_critical_allergies(self, pet_id: str) -> List[Allergy]:
        """
        Get critical (severe or life-threatening) allergies for a pet.
        
        Args:
            pet_id: Pet's ID
            
        Returns:
            List of critical Allergy instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Allergy)
                .where(
                    and_(
                        Allergy.pet_id == pet_id_uuid,
                        Allergy.severity.in_([AllergySeverity.SEVERE, AllergySeverity.LIFE_THREATENING]),
                        Allergy.is_active == True
                    )
                )
                .order_by(desc(Allergy.severity))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []


