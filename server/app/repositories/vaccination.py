"""
Vaccination repository for database operations.

This module provides the VaccinationRepository class for vaccination-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List
from datetime import date
import uuid

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from app.models.vaccination import Vaccination
from app.repositories.base import BaseRepository


class VaccinationRepository(BaseRepository[Vaccination]):
    """
    Vaccination repository for vaccination-specific database operations.
    
    This class extends BaseRepository to provide vaccination-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the vaccination repository."""
        super().__init__(Vaccination, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[Vaccination]:
        """
        Get all vaccinations for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Vaccination instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Vaccination)
                .where(Vaccination.pet_id == pet_id_uuid)
                .order_by(desc(Vaccination.administered_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_medical_record_id(self, medical_record_id: str) -> List[Vaccination]:
        """
        Get all vaccinations for a specific medical record.
        
        Args:
            medical_record_id: Medical record's ID
            
        Returns:
            List of Vaccination instances
        """
        try:
            record_id_uuid = uuid.UUID(medical_record_id)
            result = self.session.execute(
                select(Vaccination)
                .where(Vaccination.medical_record_id == record_id_uuid)
                .order_by(desc(Vaccination.administered_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_vaccine_name(self, pet_id: str, vaccine_name: str) -> List[Vaccination]:
        """
        Get vaccinations for a pet filtered by vaccine name.
        
        Args:
            pet_id: Pet's ID
            vaccine_name: Name of vaccine
            
        Returns:
            List of Vaccination instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Vaccination)
                .where(
                    and_(
                        Vaccination.pet_id == pet_id_uuid,
                        Vaccination.vaccine_name.ilike(f"%{vaccine_name}%")
                    )
                )
                .order_by(desc(Vaccination.administered_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_due_vaccinations(self, pet_id: str) -> List[Vaccination]:
        """
        Get vaccinations that are due or overdue for a pet.
        
        Args:
            pet_id: Pet's ID
            
        Returns:
            List of Vaccination instances that are due
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            today = date.today()
            result = self.session.execute(
                select(Vaccination)
                .where(
                    and_(
                        Vaccination.pet_id == pet_id_uuid,
                        Vaccination.next_due_date.isnot(None),
                        Vaccination.next_due_date <= today
                    )
                )
                .order_by(Vaccination.next_due_date)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_upcoming_vaccinations(self, pet_id: str, days: int = 30) -> List[Vaccination]:
        """
        Get vaccinations due within specified days.
        
        Args:
            pet_id: Pet's ID
            days: Number of days to look ahead
            
        Returns:
            List of Vaccination instances due soon
        """
        try:
            from datetime import timedelta
            pet_id_uuid = uuid.UUID(pet_id)
            today = date.today()
            end_date = today + timedelta(days=days)
            
            result = self.session.execute(
                select(Vaccination)
                .where(
                    and_(
                        Vaccination.pet_id == pet_id_uuid,
                        Vaccination.next_due_date.isnot(None),
                        Vaccination.next_due_date > today,
                        Vaccination.next_due_date <= end_date
                    )
                )
                .order_by(Vaccination.next_due_date)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_required_by_law(self, pet_id: str) -> List[Vaccination]:
        """
        Get legally required vaccinations for a pet.
        
        Args:
            pet_id: Pet's ID
            
        Returns:
            List of Vaccination instances required by law
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(Vaccination)
                .where(
                    and_(
                        Vaccination.pet_id == pet_id_uuid,
                        Vaccination.is_required_by_law == True
                    )
                )
                .order_by(desc(Vaccination.administered_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []


