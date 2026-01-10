"""
Medication Log repository for database operations.

This module provides the MedicationLogRepository class for managing
owner-managed medication logs in the database.
"""

from datetime import datetime, date
from typing import List, Optional
import uuid

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models.medication_log import MedicationLog
from app.repositories.base import BaseRepository


class MedicationLogRepository(BaseRepository[MedicationLog]):
    """
    Repository for medication log database operations.
    
    This class provides database access methods for owner-managed medication logs.
    """
    
    def __init__(self, session: Session) -> None:
        """
        Initialize the medication log repository.
        
        Args:
            session: Database session
        """
        super().__init__(MedicationLog, session)
    
    def get_by_pet_id(
        self,
        pet_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicationLog]:
        """
        Get all medication logs for a pet with pagination.
        
        Args:
            pet_id: Pet's unique identifier
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of medication logs
        """
        stmt = (
            select(MedicationLog)
            .where(MedicationLog.pet_id == pet_id)
            .order_by(MedicationLog.administered_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def get_recent_medications(
        self,
        pet_id: uuid.UUID,
        days: int = 7
    ) -> List[MedicationLog]:
        """
        Get recent medication logs for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            days: Number of days to look back (default: 7)
            
        Returns:
            List of recent medication logs
        """
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        stmt = (
            select(MedicationLog)
            .where(
                and_(
                    MedicationLog.pet_id == pet_id,
                    MedicationLog.administered_at >= cutoff_date
                )
            )
            .order_by(MedicationLog.administered_at.desc())
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def get_by_date_range(
        self,
        pet_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime
    ) -> List[MedicationLog]:
        """
        Get medication logs within a date range.
        
        Args:
            pet_id: Pet's unique identifier
            start_date: Start datetime of range (inclusive)
            end_date: End datetime of range (inclusive)
            
        Returns:
            List of medication logs
        """
        stmt = (
            select(MedicationLog)
            .where(
                and_(
                    MedicationLog.pet_id == pet_id,
                    MedicationLog.administered_at >= start_date,
                    MedicationLog.administered_at <= end_date
                )
            )
            .order_by(MedicationLog.administered_at.desc())
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def get_by_medication_name(
        self,
        pet_id: uuid.UUID,
        medication_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicationLog]:
        """
        Get medication logs by medication name for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            medication_name: Name of the medication
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of medication logs
        """
        stmt = (
            select(MedicationLog)
            .where(
                and_(
                    MedicationLog.pet_id == pet_id,
                    MedicationLog.medication_name.ilike(f"%{medication_name}%")
                )
            )
            .order_by(MedicationLog.administered_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def count_by_pet_id(self, pet_id: uuid.UUID) -> int:
        """
        Count total medication logs for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            
        Returns:
            Total count of medication logs
        """
        stmt = select(MedicationLog).where(MedicationLog.pet_id == pet_id)
        result = self.session.execute(stmt)
        return len(list(result.scalars().all()))
    
    def update(self, log_id: uuid.UUID, **kwargs) -> Optional[MedicationLog]:
        """
        Update a medication log.
        
        Args:
            log_id: Medication log unique identifier
            **kwargs: Fields to update
            
        Returns:
            Updated medication log or None if not found
        """
        log = self.get_by_id(log_id)
        if not log:
            return None
        
        for key, value in kwargs.items():
            if hasattr(log, key):
                setattr(log, key, value)
        
        return self.update_entity(log)
    
    def delete(self, log_id: uuid.UUID) -> bool:
        """
        Delete a medication log.
        
        Args:
            log_id: Medication log unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        log = self.get_by_id(log_id)
        if not log:
            return False
        
        self.delete_entity(log)
        return True

