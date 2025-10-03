"""
Medical Record Attachment model for the application.

This module defines the MedicalRecordAttachment SQLAlchemy model representing
files and images associated with medical records.
"""

from datetime import datetime
from typing import Optional
import uuid
import enum

from sqlalchemy import Column, DateTime, String, Text, BigInteger, UUID, ForeignKey, Enum
from sqlalchemy.sql import func

from app.database import Base


class AttachmentType(str, enum.Enum):
    """Attachment type enumeration."""
    LAB_RESULT = "lab_result"
    XRAY = "xray"
    ULTRASOUND = "ultrasound"
    CERTIFICATE = "certificate"
    REPORT = "report"
    PHOTO = "photo"
    OTHER = "other"


class MedicalRecordAttachment(Base):
    """
    Medical Record Attachment model for files associated with medical records.
    
    Attributes:
        id: Primary key identifier (UUID)
        medical_record_id: ID of the associated medical record (optional)
        lab_test_id: ID of the associated lab test (optional)
        vaccination_id: ID of the associated vaccination (optional)
        pet_id: ID of the pet (denormalized for queries)
        file_name: Original filename
        file_url: Storage URL (e.g., S3)
        file_type: MIME type
        file_size: Size in bytes
        attachment_type: Type of attachment
        description: Description of the attachment (optional)
        uploaded_by_user_id: User who uploaded the file
        uploaded_by_role: Role at time of upload
        created_at: Attachment record creation timestamp
    """
    
    __tablename__ = "medical_record_attachments"
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medical_record_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("medical_records.id"), 
        nullable=True,
        index=True
    )
    lab_test_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("lab_tests.id"), 
        nullable=True,
        index=True
    )
    vaccination_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("vaccinations.id"), 
        nullable=True,
        index=True
    )
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    file_name: str = Column(String(255), nullable=False)
    file_url: str = Column(String(500), nullable=False)
    file_type: str = Column(String(50), nullable=False)
    file_size: int = Column(BigInteger, nullable=False)
    attachment_type: str = Column(
        Enum(AttachmentType), 
        default=AttachmentType.OTHER, 
        nullable=False,
        index=True
    )
    description: Optional[str] = Column(Text, nullable=True)
    uploaded_by_user_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.public_id"), 
        nullable=False
    )
    uploaded_by_role: str = Column(String(50), nullable=False)
    created_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the MedicalRecordAttachment model."""
        return f"<MedicalRecordAttachment(id={self.id}, file_name='{self.file_name}')>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "medical_record_id": str(self.medical_record_id) if self.medical_record_id else None,
            "lab_test_id": str(self.lab_test_id) if self.lab_test_id else None,
            "vaccination_id": str(self.vaccination_id) if self.vaccination_id else None,
            "pet_id": str(self.pet_id),
            "file_name": self.file_name,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "attachment_type": self.attachment_type.value if self.attachment_type else None,
            "description": self.description,
            "uploaded_by_user_id": str(self.uploaded_by_user_id),
            "uploaded_by_role": self.uploaded_by_role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


