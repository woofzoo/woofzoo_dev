"""
Clinic Workflow Service for clinic operations.

This service handles clinic-specific workflows including:
- Pet search (by email, phone, pet_id)
- OTP verification and access management
- Pre-check vitals recording
- Doctor assignment and queue management
"""

from typing import Optional, Tuple
from datetime import datetime, timezone, timedelta
import uuid
import secrets

from sqlalchemy.orm import Session

from app.models.pet import Pet
from app.models.user import User
from app.models.pet_clinic_access import PetClinicAccess, QueueStatus, AccessStatus
from app.models.otp import OTP, OTPPurpose
from app.models.medical_record import MedicalRecord
from app.repositories.pet import PetRepository
from app.repositories.user import UserRepository
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.repositories.otp import OTPRepository
from app.repositories.medical_record import MedicalRecordRepository
from app.services.email import EmailService
from app.logger import logger
from app.config import settings


class ClinicWorkflowService:
    """Service for clinic workflow operations."""
    
    def __init__(
        self,
        db: Session,
        pet_repository: PetRepository,
        user_repository: UserRepository,
        pet_clinic_access_repository: PetClinicAccessRepository,
        otp_repository: OTPRepository,
        medical_record_repository: MedicalRecordRepository,
        email_service: EmailService
    ):
        """Initialize the clinic workflow service."""
        self.db = db
        self.pet_repository = pet_repository
        self.user_repository = user_repository
        self.pet_clinic_access_repository = pet_clinic_access_repository
        self.otp_repository = otp_repository
        self.medical_record_repository = medical_record_repository
        self.email_service = email_service
    
    def search_pet(
        self, 
        search_type: str, 
        search_value: str,
        clinic_user_id: uuid.UUID
    ) -> Optional[Tuple[Pet, User]]:
        """
        Search for a pet by owner email, phone, or pet_id.
        
        Args:
            search_type: Type of search ('email', 'phone', 'pet_id')
            search_value: Value to search for
            clinic_user_id: UUID of the clinic user performing the search
            
        Returns:
            Tuple[Pet, User] if found, None otherwise
            
        Raises:
            ValueError: If search_type is invalid
        """
        logger.info(
            "Pet search initiated",
            extra={
                "search_type": search_type,
                "search_value": search_value,
                "clinic_user_id": str(clinic_user_id)
            }
        )
        
        pet: Optional[Pet] = None
        owner: Optional[User] = None
        
        if search_type == "email":
            # Search by owner email
            owner = self.user_repository.get_by_email(search_value)
            if owner:
                # Get first active pet owned by this user
                pets = self.pet_repository.get_by_owner_id(owner.public_id)
                if pets:
                    pet = pets[0]  # For now, return first pet
        
        elif search_type == "phone":
            # Search by owner phone
            owner = self.user_repository.get_by_phone(search_value)
            if owner:
                pets = self.pet_repository.get_by_owner_id(owner.public_id)
                if pets:
                    pet = pets[0]
        
        elif search_type == "pet_id":
            # Search by pet_id
            pet = self.pet_repository.get_by_pet_id(search_value)
            if pet:
                # Get owner
                owner = self.user_repository.get_by_public_id(pet.owner_id)
        
        else:
            raise ValueError(f"Invalid search_type: {search_type}")
        
        if pet and owner:
            logger.info(
                "Pet found",
                extra={
                    "pet_id": pet.pet_id,
                    "owner_id": str(owner.public_id),
                    "search_type": search_type
                }
            )
            return pet, owner
        else:
            logger.info(
                "Pet not found",
                extra={
                    "search_type": search_type,
                    "search_value": search_value
                }
            )
            return None
    
    def request_otp_for_visit(
        self,
        pet_id: uuid.UUID,
        clinic_id: uuid.UUID,
        clinic_user_id: uuid.UUID,
        purpose: str = "Clinic visit and doctor assignment"
    ) -> Tuple[OTP, str]:
        """
        Request OTP for clinic visit access.
        
        Args:
            pet_id: UUID of the pet
            clinic_id: UUID of the clinic
            clinic_user_id: UUID of the clinic user requesting OTP
            purpose: Purpose of the OTP
            
        Returns:
            Tuple[OTP, str]: (OTP record, owner_email)
            
        Raises:
            ValueError: If pet not found or owner not found
        """
        # Get pet and owner
        pet = self.pet_repository.get(pet_id)
        if not pet:
            raise ValueError("Pet not found")
        
        owner = self.user_repository.get_by_public_id(pet.owner_id)
        if not owner:
            raise ValueError("Pet owner not found")
        
        # Generate 6-digit OTP
        otp_code = ''.join(secrets.choice('0123456789') for _ in range(6))
        
        # Calculate expiry
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expire_minutes)
        
        # Create OTP record
        otp = self.otp_repository.create(
            user_id=owner.public_id,
            otp_code=otp_code,
            purpose=OTPPurpose.PET_ACCESS,
            expires_at=expires_at,
            metadata={
                "pet_id": str(pet_id),
                "clinic_id": str(clinic_id),
                "clinic_user_id": str(clinic_user_id),
                "purpose": purpose
            }
        )
        
        # Send OTP email
        try:
            email_sent = self.email_service.send_clinic_access_otp_email(
                to_email=owner.email,
                to_name=owner.full_name,
                otp_code=otp_code,
                pet_name=pet.name,
                clinic_name="Clinic",  # TODO: Get actual clinic name
                expires_in_minutes=settings.otp_expire_minutes
            )
            
            if email_sent:
                logger.info(
                    "Clinic access OTP sent",
                    extra={
                        "owner_email": owner.email,
                        "pet_id": str(pet_id),
                        "otp_id": str(otp.id)
                    }
                )
            else:
                logger.warning(
                    "Failed to send clinic access OTP email",
                    extra={"owner_email": owner.email, "pet_id": str(pet_id)}
                )
        except Exception as e:
            logger.exception(
                "Error sending clinic access OTP email",
                extra={"owner_email": owner.email, "pet_id": str(pet_id), "error": str(e)}
            )
        
        return otp, owner.email
    
    def verify_otp_and_create_access(
        self,
        pet_id: uuid.UUID,
        clinic_id: uuid.UUID,
        otp_code: str,
        clinic_user_id: uuid.UUID
    ) -> PetClinicAccess:
        """
        Verify OTP and create clinic access record.
        
        Args:
            pet_id: UUID of the pet
            clinic_id: UUID of the clinic
            otp_code: OTP code to verify
            clinic_user_id: UUID of the clinic user
            
        Returns:
            PetClinicAccess: Created access record
            
        Raises:
            ValueError: If OTP is invalid, expired, or already used
        """
        # Get pet and owner
        pet = self.pet_repository.get(pet_id)
        if not pet:
            raise ValueError("Pet not found")
        
        owner = self.user_repository.get_by_public_id(pet.owner_id)
        if not owner:
            raise ValueError("Pet owner not found")
        
        # Verify OTP
        otp = self.otp_repository.get_by_code_and_user(otp_code, owner.public_id)
        if not otp:
            raise ValueError("Invalid OTP code")
        
        if otp.is_used:
            raise ValueError("OTP has already been used")
        
        if otp.is_expired:
            raise ValueError("OTP has expired")
        
        if otp.purpose != OTPPurpose.PET_ACCESS:
            raise ValueError("Invalid OTP purpose")
        
        # Mark OTP as used
        self.otp_repository.mark_used(otp.id)
        
        # Create access record
        access = self.pet_clinic_access_repository.create(
            pet_id=pet_id,
            clinic_id=clinic_id,
            access_type="CLINIC_VISIT",
            granted_by_user_id=owner.public_id,
            otp_id=otp.id,
            purpose="Clinic visit with doctor assignment",
            status=AccessStatus.ACTIVE,
            queue_status=QueueStatus.PENDING_PRECHECK
        )
        
        logger.info(
            "Clinic access created after OTP verification",
            extra={
                "access_id": str(access.id),
                "pet_id": str(pet_id),
                "clinic_id": str(clinic_id),
                "queue_status": access.queue_status
            }
        )
        
        return access
    
    def update_pre_check_vitals(
        self,
        access_record_id: uuid.UUID,
        clinic_user_id: uuid.UUID,
        weight: Optional[float] = None,
        temperature: Optional[float] = None,
        heart_rate: Optional[int] = None,
        respiratory_rate: Optional[int] = None,
        notes: Optional[str] = None
    ) -> PetClinicAccess:
        """
        Update pre-check vitals for a pet.
        
        Args:
            access_record_id: UUID of the access record
            clinic_user_id: UUID of the clinic user updating vitals
            weight: Weight in kg
            temperature: Temperature in °C
            heart_rate: Heart rate in BPM
            respiratory_rate: Respiratory rate
            notes: Pre-check observations
            
        Returns:
            PetClinicAccess: Updated access record
            
        Raises:
            ValueError: If access record not found or invalid status
        """
        # Get access record
        access = self.pet_clinic_access_repository.get(access_record_id)
        if not access:
            raise ValueError("Access record not found")
        
        if access.status != AccessStatus.ACTIVE:
            raise ValueError("Access record is not active")
        
        if access.queue_status != QueueStatus.PENDING_PRECHECK:
            raise ValueError(f"Cannot update pre-checks. Current status: {access.queue_status}")
        
        # Update pre-check fields
        access.pre_check_weight = weight
        access.pre_check_temperature = temperature
        access.pre_check_heart_rate = heart_rate
        access.pre_check_respiratory_rate = respiratory_rate
        access.pre_check_notes = notes
        access.pre_check_completed_at = datetime.now(timezone.utc)
        access.pre_check_by_user_id = clinic_user_id
        
        # Update queue status to ready for doctor
        access.queue_status = QueueStatus.READY_FOR_DOCTOR
        
        self.db.commit()
        self.db.refresh(access)
        
        logger.info(
            "Pre-check vitals updated",
            extra={
                "access_id": str(access_record_id),
                "clinic_user_id": str(clinic_user_id),
                "queue_status": access.queue_status
            }
        )
        
        return access
    
    def assign_to_doctor(
        self,
        access_record_id: uuid.UUID,
        doctor_id: uuid.UUID,
        visit_type: str,
        chief_complaint: Optional[str] = None
    ) -> Tuple[PetClinicAccess, MedicalRecord]:
        """
        Assign pet to doctor and create medical record.
        
        Args:
            access_record_id: UUID of the access record
            doctor_id: UUID of the doctor profile
            visit_type: Type of visit
            chief_complaint: Reason for visit
            
        Returns:
            Tuple[PetClinicAccess, MedicalRecord]: (Updated access record, Created medical record)
            
        Raises:
            ValueError: If access record not found or invalid status
        """
        # Get access record
        access = self.pet_clinic_access_repository.get(access_record_id)
        if not access:
            raise ValueError("Access record not found")
        
        if access.status != AccessStatus.ACTIVE:
            raise ValueError("Access record is not active")
        
        if access.queue_status != QueueStatus.READY_FOR_DOCTOR:
            raise ValueError(f"Pet not ready for doctor assignment. Current status: {access.queue_status}")
        
        # Create medical record
        medical_record = self.medical_record_repository.create(
            pet_id=access.pet_id,
            doctor_id=doctor_id,
            visit_date=datetime.now(timezone.utc),
            visit_type=visit_type,
            chief_complaint=chief_complaint or "Clinic visit",
            vital_signs={
                "weight": access.pre_check_weight,
                "temperature": access.pre_check_temperature,
                "heart_rate": access.pre_check_heart_rate,
                "respiratory_rate": access.pre_check_respiratory_rate
            } if any([
                access.pre_check_weight,
                access.pre_check_temperature,
                access.pre_check_heart_rate,
                access.pre_check_respiratory_rate
            ]) else None
        )
        
        # Update access record
        access.medical_record_id = medical_record.id
        access.queue_status = QueueStatus.WITH_DOCTOR
        access.assigned_to_doctor_at = datetime.now(timezone.utc)
        
        # Calculate queue position (simple: count active pets with doctor)
        active_count = self.db.query(PetClinicAccess).filter(
            PetClinicAccess.queue_status == QueueStatus.WITH_DOCTOR,
            PetClinicAccess.assigned_to_doctor_at <= access.assigned_to_doctor_at
        ).count()
        access.queue_position = active_count
        
        self.db.commit()
        self.db.refresh(access)
        self.db.refresh(medical_record)
        
        logger.info(
            "Pet assigned to doctor",
            extra={
                "access_id": str(access_record_id),
                "doctor_id": str(doctor_id),
                "medical_record_id": str(medical_record.id),
                "queue_position": access.queue_position
            }
        )
        
        return access, medical_record

