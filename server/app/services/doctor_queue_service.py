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
        pet_clinic_access_repository: PetClinicAccessRepository,
        medical_record_repository: MedicalRecordRepository,
        pet_repository: PetRepository,
        user_repository: UserRepository
    ):
        """Initialize the doctor queue service."""
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
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(tomorrow, datetime.min.time())
        
        # Use repository method to get queue items
        queue_items = self.pet_clinic_access_repository.get_todays_queue_for_doctor(
            doctor_id=doctor_id,
            start_date=start_date,
            end_date=end_date
        )
        
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
        
        # Get medical history using repository method
        medical_history = self.medical_record_repository.get_medical_history_excluding(
            pet_id=pet.id,
            exclude_record_id=medical_record_id,
            limit=10
        )
        
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
        
        # Prepare vital signs update
        vital_signs_update = {}
        if weight:
            vital_signs_update["weight"] = weight
        if temperature:
            vital_signs_update["temperature"] = temperature
        if vital_signs:
            vital_signs_update.update(vital_signs)
        
        # Use repository method to update
        medical_record = self.medical_record_repository.update_visit_record(
            medical_record_id=medical_record_id,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            clinical_notes=clinical_notes,
            vital_signs_update=vital_signs_update if vital_signs_update else None
        )
        
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
        
        # Update medical record with follow-up info using repository method
        if follow_up_required:
            medical_record = self.medical_record_repository.update_follow_up(
                medical_record_id=medical_record_id,
                follow_up_date=follow_up_date,
                follow_up_notes=follow_up_notes
            )
        
        # Use repository method to complete visit
        access = self.pet_clinic_access_repository.complete_visit(
            medical_record_id=medical_record_id,
            completed_at=datetime.now(timezone.utc)
        )
        
        logger.info(
            "Visit marked as complete",
            extra={
                "medical_record_id": str(medical_record_id),
                "doctor_id": str(doctor_id),
                "follow_up_required": follow_up_required
            }
        )
        
        return medical_record, access

