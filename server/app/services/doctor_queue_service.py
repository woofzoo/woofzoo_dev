"""
Doctor Queue Service for doctor-specific operations.

This service handles doctor queue management including:
- Viewing today's queue
- Getting pet visit details
- Updating medical records
- Completing visits
"""

from typing import List, Tuple, Optional
from datetime import datetime, timezone, date, timedelta
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.pet_clinic_access import PetClinicAccess, QueueStatus
from app.models.medical_record import MedicalRecord
from app.models.pet import Pet
from app.models.user import User
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.repositories.medical_record import MedicalRecordRepository
from app.repositories.pet import PetRepository
from app.repositories.user import UserRepository
from app.logger import logger


class DoctorQueueService:
    """Service for doctor queue operations."""
    
    def __init__(
        self,
        db: Session,
        pet_clinic_access_repository: PetClinicAccessRepository,
        medical_record_repository: MedicalRecordRepository,
        pet_repository: PetRepository,
        user_repository: UserRepository
    ):
        """Initialize the doctor queue service."""
        self.db = db
        self.pet_clinic_access_repository = pet_clinic_access_repository
        self.medical_record_repository = medical_record_repository
        self.pet_repository = pet_repository
        self.user_repository = user_repository
    
    def get_todays_queue(
        self,
        doctor_id: uuid.UUID
    ) -> Tuple[List[PetClinicAccess], dict]:
        """
        Get today's queue for a doctor.
        
        Args:
            doctor_id: UUID of the doctor profile
            
        Returns:
            Tuple[List[PetClinicAccess], dict]: (queue items, statistics)
        """
        today = datetime.now(timezone.utc).date()
        tomorrow = today + timedelta(days=1)
        
        # Query all access records assigned to this doctor today
        queue_items = self.db.query(PetClinicAccess).filter(
            and_(
                PetClinicAccess.medical_record_id.isnot(None),
                PetClinicAccess.assigned_to_doctor_at >= datetime.combine(today, datetime.min.time()),
                PetClinicAccess.assigned_to_doctor_at < datetime.combine(tomorrow, datetime.min.time()),
                PetClinicAccess.queue_status.in_([QueueStatus.WITH_DOCTOR, QueueStatus.COMPLETED])
            )
        ).join(
            MedicalRecord,
            PetClinicAccess.medical_record_id == MedicalRecord.id
        ).filter(
            MedicalRecord.doctor_id == doctor_id
        ).order_by(
            PetClinicAccess.queue_position
        ).all()
        
        # Calculate statistics
        total = len(queue_items)
        completed = sum(1 for item in queue_items if item.queue_status == QueueStatus.COMPLETED)
        in_progress = sum(1 for item in queue_items if item.queue_status == QueueStatus.WITH_DOCTOR)
        
        statistics = {
            "total": total,
            "completed": completed,
            "in_progress": in_progress
        }
        
        logger.info(
            "Doctor queue retrieved",
            extra={
                "doctor_id": str(doctor_id),
                "date": str(today),
                **statistics
            }
        )
        
        return queue_items, statistics
    
    def get_visit_details(
        self,
        medical_record_id: uuid.UUID,
        doctor_id: uuid.UUID
    ) -> Tuple[Pet, MedicalRecord, User, List[MedicalRecord]]:
        """
        Get detailed information for a visit.
        
        Args:
            medical_record_id: UUID of the medical record
            doctor_id: UUID of the doctor (for authorization)
            
        Returns:
            Tuple[Pet, MedicalRecord, User, List[MedicalRecord]]: 
                (pet, current_record, owner, medical_history)
                
        Raises:
            ValueError: If record not found or doctor not authorized
        """
        # Get medical record
        medical_record = self.medical_record_repository.get(medical_record_id)
        if not medical_record:
            raise ValueError("Medical record not found")
        
        # Verify doctor authorization
        if medical_record.doctor_id != doctor_id:
            raise ValueError("Not authorized to access this medical record")
        
        # Get pet
        pet = self.pet_repository.get(medical_record.pet_id)
        if not pet:
            raise ValueError("Pet not found")
        
        # Get owner
        owner = self.user_repository.get_by_public_id(pet.owner_id)
        if not owner:
            raise ValueError("Pet owner not found")
        
        # Get medical history (excluding current visit)
        medical_history = self.db.query(MedicalRecord).filter(
            and_(
                MedicalRecord.pet_id == pet.id,
                MedicalRecord.id != medical_record_id
            )
        ).order_by(
            MedicalRecord.visit_date.desc()
        ).limit(10).all()
        
        logger.info(
            "Visit details retrieved",
            extra={
                "medical_record_id": str(medical_record_id),
                "doctor_id": str(doctor_id),
                "pet_id": pet.pet_id
            }
        )
        
        return pet, medical_record, owner, medical_history
    
    def update_visit_details(
        self,
        medical_record_id: uuid.UUID,
        doctor_id: uuid.UUID,
        diagnosis: Optional[str] = None,
        treatment_plan: Optional[str] = None,
        clinical_notes: Optional[str] = None,
        weight: Optional[float] = None,
        temperature: Optional[float] = None,
        vital_signs: Optional[dict] = None
    ) -> MedicalRecord:
        """
        Update visit details.
        
        Args:
            medical_record_id: UUID of the medical record
            doctor_id: UUID of the doctor
            diagnosis: Diagnosis text
            treatment_plan: Treatment plan
            clinical_notes: Clinical notes
            weight: Weight in kg
            temperature: Temperature in °C
            vital_signs: Additional vital signs
            
        Returns:
            MedicalRecord: Updated medical record
            
        Raises:
            ValueError: If record not found or doctor not authorized
        """
        # Get medical record
        medical_record = self.medical_record_repository.get(medical_record_id)
        if not medical_record:
            raise ValueError("Medical record not found")
        
        # Verify doctor authorization
        if medical_record.doctor_id != doctor_id:
            raise ValueError("Not authorized to update this medical record")
        
        # Update fields
        if diagnosis is not None:
            medical_record.diagnosis = diagnosis
        if treatment_plan is not None:
            medical_record.treatment_plan = treatment_plan
        if clinical_notes is not None:
            medical_record.clinical_notes = clinical_notes
        
        # Update vital signs
        if weight or temperature or vital_signs:
            existing_vitals = medical_record.vital_signs or {}
            if weight:
                existing_vitals["weight"] = weight
            if temperature:
                existing_vitals["temperature"] = temperature
            if vital_signs:
                existing_vitals.update(vital_signs)
            medical_record.vital_signs = existing_vitals
        
        self.db.commit()
        self.db.refresh(medical_record)
        
        logger.info(
            "Visit details updated",
            extra={
                "medical_record_id": str(medical_record_id),
                "doctor_id": str(doctor_id)
            }
        )
        
        return medical_record
    
    def complete_visit(
        self,
        medical_record_id: uuid.UUID,
        doctor_id: uuid.UUID,
        follow_up_required: bool = False,
        follow_up_date: Optional[date] = None,
        follow_up_notes: Optional[str] = None
    ) -> Tuple[MedicalRecord, PetClinicAccess]:
        """
        Mark visit as complete and remove from active queue.
        
        Args:
            medical_record_id: UUID of the medical record
            doctor_id: UUID of the doctor
            follow_up_required: Whether follow-up is needed
            follow_up_date: Date for follow-up
            follow_up_notes: Follow-up instructions
            
        Returns:
            Tuple[MedicalRecord, PetClinicAccess]: (updated record, updated access)
            
        Raises:
            ValueError: If record not found or doctor not authorized
        """
        # Get medical record
        medical_record = self.medical_record_repository.get(medical_record_id)
        if not medical_record:
            raise ValueError("Medical record not found")
        
        # Verify doctor authorization
        if medical_record.doctor_id != doctor_id:
            raise ValueError("Not authorized to complete this visit")
        
        # Update medical record with follow-up info
        if follow_up_required:
            medical_record.follow_up_date = follow_up_date
            medical_record.follow_up_notes = follow_up_notes
        
        # Find associated access record
        access = self.db.query(PetClinicAccess).filter(
            PetClinicAccess.medical_record_id == medical_record_id
        ).first()
        
        if access:
            # Update access record
            access.queue_status = QueueStatus.COMPLETED
            access.visit_completed_at = datetime.now(timezone.utc)
        
        self.db.commit()
        self.db.refresh(medical_record)
        if access:
            self.db.refresh(access)
        
        logger.info(
            "Visit marked as complete",
            extra={
                "medical_record_id": str(medical_record_id),
                "doctor_id": str(doctor_id),
                "follow_up_required": follow_up_required
            }
        )
        
        return medical_record, access

