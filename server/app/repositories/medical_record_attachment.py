"""
Medical Record Attachment repository for database operations.

This module provides the MedicalRecordAttachmentRepository class for
attachment-specific database operations extending the base repository functionality.
"""

from typing import Optional, List
import uuid

from sqlalchemy import select, or_, and_, desc
from sqlalchemy.orm import Session

from app.models.medical_record_attachment import MedicalRecordAttachment, AttachmentType
from app.repositories.base import BaseRepository


class MedicalRecordAttachmentRepository(BaseRepository[MedicalRecordAttachment]):
    """
    Medical Record Attachment repository for attachment-specific database operations.
    
    This class extends BaseRepository to provide attachment-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the medical record attachment repository."""
        super().__init__(MedicalRecordAttachment, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[MedicalRecordAttachment]:
        """
        Get all attachments for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecordAttachment instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(MedicalRecordAttachment)
                .where(MedicalRecordAttachment.pet_id == pet_id_uuid)
                .order_by(desc(MedicalRecordAttachment.created_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_medical_record_id(self, medical_record_id: str) -> List[MedicalRecordAttachment]:
        """
        Get all attachments for a specific medical record.
        
        Args:
            medical_record_id: Medical record's ID
            
        Returns:
            List of MedicalRecordAttachment instances
        """
        try:
            record_id_uuid = uuid.UUID(medical_record_id)
            result = self.session.execute(
                select(MedicalRecordAttachment)
                .where(MedicalRecordAttachment.medical_record_id == record_id_uuid)
                .order_by(desc(MedicalRecordAttachment.created_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_lab_test_id(self, lab_test_id: str) -> List[MedicalRecordAttachment]:
        """
        Get all attachments for a specific lab test.
        
        Args:
            lab_test_id: Lab test's ID
            
        Returns:
            List of MedicalRecordAttachment instances
        """
        try:
            lab_test_id_uuid = uuid.UUID(lab_test_id)
            result = self.session.execute(
                select(MedicalRecordAttachment)
                .where(MedicalRecordAttachment.lab_test_id == lab_test_id_uuid)
                .order_by(desc(MedicalRecordAttachment.created_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_vaccination_id(self, vaccination_id: str) -> List[MedicalRecordAttachment]:
        """
        Get all attachments for a specific vaccination.
        
        Args:
            vaccination_id: Vaccination's ID
            
        Returns:
            List of MedicalRecordAttachment instances
        """
        try:
            vaccination_id_uuid = uuid.UUID(vaccination_id)
            result = self.session.execute(
                select(MedicalRecordAttachment)
                .where(MedicalRecordAttachment.vaccination_id == vaccination_id_uuid)
                .order_by(desc(MedicalRecordAttachment.created_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_attachment_type(
        self, 
        pet_id: str, 
        attachment_type: AttachmentType, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[MedicalRecordAttachment]:
        """
        Get attachments for a pet filtered by type.
        
        Args:
            pet_id: Pet's ID
            attachment_type: Type of attachment to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecordAttachment instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(MedicalRecordAttachment)
                .where(
                    and_(
                        MedicalRecordAttachment.pet_id == pet_id_uuid,
                        MedicalRecordAttachment.attachment_type == attachment_type
                    )
                )
                .order_by(desc(MedicalRecordAttachment.created_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []


