"""
Lab Test model for the application.

This module defines the LabTest SQLAlchemy model representing
laboratory tests and their results.
"""

from datetime import datetime
from typing import Optional
import uuid
import enum

from sqlalchemy import Column, DateTime, String, Text, Boolean, UUID, ForeignKey, JSON, Enum, Index
from sqlalchemy.sql import func

from app.database import Base


class TestStatus(str, enum.Enum):
    """Test status enumeration."""
    ORDERED = "ordered"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LabTest(Base):
    """
    Lab Test model representing laboratory tests and results.
    
    Attributes:
        id: Primary key identifier (UUID)
        medical_record_id: ID of the associated medical visit (optional)
        pet_id: ID of the pet tested
        test_name: Name of the test
        test_type: Type of test (e.g., "Blood Work", "X-Ray")
        ordered_by_doctor_id: ID of the doctor who ordered the test
        ordered_at: When the test was ordered
        performed_at: When the test was performed (optional)
        performed_by_clinic_id: ID of the lab/clinic that performed test
        status: Current status of the test
        results: Test results as text
        results_json: Structured test results (JSONB)
        results_file_url: URL to results file (PDF/image)
        reference_ranges: Normal value ranges (JSONB)
        abnormal_flags: Flags for abnormal values (JSONB)
        interpretation: Doctor's interpretation of results
        is_abnormal: Quick flag for abnormal results
        created_at: Test record creation timestamp
        updated_at: Test record last update timestamp
    """
    
    __tablename__ = "lab_tests"
    __table_args__ = (
        Index('idx_ordered_at_desc', 'ordered_at', postgresql_ops={'ordered_at': 'DESC'}),
    )
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medical_record_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("medical_records.id"), 
        nullable=True,
        index=True
    )
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    test_name: str = Column(String(200), nullable=False)
    test_type: str = Column(String(100), nullable=False)
    ordered_by_doctor_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("doctor_profiles.id"), 
        nullable=False,
        index=True
    )
    ordered_at: datetime = Column(DateTime, nullable=False, index=True)
    performed_at: Optional[datetime] = Column(DateTime, nullable=True)
    performed_by_clinic_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True), 
        ForeignKey("clinic_profiles.id"), 
        nullable=True
    )
    status: str = Column(
        Enum(TestStatus), 
        default=TestStatus.ORDERED, 
        nullable=False,
        index=True
    )
    results: Optional[str] = Column(Text, nullable=True)
    results_json: dict = Column(JSON, nullable=False, default=dict)
    results_file_url: Optional[str] = Column(String(500), nullable=True)
    reference_ranges: dict = Column(JSON, nullable=False, default=dict)
    abnormal_flags: dict = Column(JSON, nullable=False, default=dict)
    interpretation: Optional[str] = Column(Text, nullable=True)
    is_abnormal: bool = Column(Boolean, default=False, nullable=False)
    created_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: datetime = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the LabTest model."""
        return f"<LabTest(id={self.id}, test_name='{self.test_name}', pet_id={self.pet_id})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "medical_record_id": str(self.medical_record_id) if self.medical_record_id else None,
            "pet_id": str(self.pet_id),
            "test_name": self.test_name,
            "test_type": self.test_type,
            "ordered_by_doctor_id": str(self.ordered_by_doctor_id),
            "ordered_at": self.ordered_at.isoformat() if self.ordered_at else None,
            "performed_at": self.performed_at.isoformat() if self.performed_at else None,
            "performed_by_clinic_id": str(self.performed_by_clinic_id) if self.performed_by_clinic_id else None,
            "status": self.status.value if self.status else None,
            "results": self.results,
            "results_json": self.results_json,
            "results_file_url": self.results_file_url,
            "reference_ranges": self.reference_ranges,
            "abnormal_flags": self.abnormal_flags,
            "interpretation": self.interpretation,
            "is_abnormal": self.is_abnormal,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


