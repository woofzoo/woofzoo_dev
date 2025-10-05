"""
Medical Record model for the application.

This module defines the MedicalRecord SQLAlchemy model representing
pet medical visits and consultations.
"""

from datetime import datetime, date
from typing import Optional
import uuid
import enum

from sqlalchemy import Column, DateTime, Date, String, Text, Float, Boolean, UUID, ForeignKey, JSON, Enum, Index
from sqlalchemy.sql import func

from app.database import Base


class VisitType(str, enum.Enum):
    """Visit type enumeration."""
    ROUTINE_CHECKUP = "routine_checkup"
    EMERGENCY = "emergency"
    SURGERY = "surgery"
    VACCINATION = "vaccination"
    FOLLOW_UP = "follow_up"
    OTHER = "other"


class MedicalRecord(Base):
    """
    Medical Record model representing a pet's medical visit/consultation.
    
    Attributes:
        id: Primary key identifier (UUID)
        pet_id: ID of the pet this record belongs to
        visit_date: Date and time of the visit
        clinic_id: ID of the clinic where visit occurred
        doctor_id: ID of the attending doctor
        visit_type: Type of visit
        chief_complaint: Presenting problem/reason for visit
        diagnosis: Doctor's diagnosis
        symptoms: Array of symptoms observed (JSONB)
        treatment_plan: Recommended treatment
        clinical_notes: Detailed doctor notes
        weight: Pet weight at visit (kg)
        temperature: Body temperature (°C)
        vital_signs: Heart rate, respiratory rate, etc. (JSONB)
        follow_up_required: Whether follow-up is needed
        follow_up_date: Recommended follow-up date
        follow_up_notes: Follow-up instructions
        is_emergency: Was this an emergency visit
        created_by_user_id: User who created the record
        created_by_role: Role at time of creation
        created_at: Record creation timestamp (immutable)
        updated_at: Record last update timestamp
    """
    
    __tablename__ = "medical_records"
    __table_args__ = (
        Index('idx_pet_visit_date', 'pet_id', 'visit_date', postgresql_ops={'visit_date': 'DESC'}),
    )
    
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id"), 
        nullable=False,
        index=True
    )
    visit_date: datetime = Column(DateTime, nullable=False, index=True)
    clinic_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("clinic_profiles.id"), 
        nullable=False,
        index=True
    )
    doctor_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("doctor_profiles.id"), 
        nullable=False,
        index=True
    )
    visit_type: str = Column(
        Enum(VisitType), 
        default=VisitType.ROUTINE_CHECKUP, 
        nullable=False,
        index=True
    )
    chief_complaint: Optional[str] = Column(Text, nullable=True)
    diagnosis: Optional[str] = Column(Text, nullable=True)
    symptoms: dict = Column(JSON, nullable=False, default=dict)
    treatment_plan: Optional[str] = Column(Text, nullable=True)
    clinical_notes: Optional[str] = Column(Text, nullable=True)
    weight: Optional[float] = Column(Float, nullable=True)
    temperature: Optional[float] = Column(Float, nullable=True)
    vital_signs: dict = Column(JSON, nullable=False, default=dict)
    follow_up_required: bool = Column(Boolean, default=False, nullable=False)
    follow_up_date: Optional[date] = Column(Date, nullable=True)
    follow_up_notes: Optional[str] = Column(Text, nullable=True)
    is_emergency: bool = Column(Boolean, default=False, nullable=False)
    created_by_user_id: uuid.UUID = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.public_id"), 
        nullable=False
    )
    created_by_role: str = Column(String(50), nullable=False)
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
        """String representation of the MedicalRecord model."""
        return f"<MedicalRecord(id={self.id}, pet_id={self.pet_id}, visit_date={self.visit_date})>"
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "pet_id": str(self.pet_id),
            "visit_date": self.visit_date.isoformat() if self.visit_date else None,
            "clinic_id": str(self.clinic_id),
            "doctor_id": str(self.doctor_id),
            "visit_type": self.visit_type.value if self.visit_type else None,
            "chief_complaint": self.chief_complaint,
            "diagnosis": self.diagnosis,
            "symptoms": self.symptoms,
            "treatment_plan": self.treatment_plan,
            "clinical_notes": self.clinical_notes,
            "weight": self.weight,
            "temperature": self.temperature,
            "vital_signs": self.vital_signs,
            "follow_up_required": self.follow_up_required,
            "follow_up_date": self.follow_up_date.isoformat() if self.follow_up_date else None,
            "follow_up_notes": self.follow_up_notes,
            "is_emergency": self.is_emergency,
            "created_by_user_id": str(self.created_by_user_id),
            "created_by_role": self.created_by_role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


