"""
Clinic Access Service for OTP-based access control.

This module provides the ClinicAccessService class for managing
OTP-based clinic access to pet medical records.
"""

from typing import Optional
from datetime import datetime, timedelta
import uuid
import random
import string

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.otp import OTP, OTPPurpose
from app.models.pet_clinic_access import PetClinicAccess, AccessStatus
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.repositories.pet import PetRepository
from app.schemas.pet_clinic_access import PetClinicAccessRequest, PetClinicAccessGrant


class ClinicAccessService:
    """
    Clinic Access service for OTP-based access control.
    
    This class handles business logic for granting/revoking clinic access
    to pet medical records via OTP validation.
    """
    
    def __init__(
        self,
        session: Session,
        pet_clinic_access_repository: PetClinicAccessRepository,
        pet_repository: PetRepository
    ):
        """Initialize the clinic access service."""
        self.session = session
        self.pet_clinic_access_repository = pet_clinic_access_repository
        self.pet_repository = pet_repository
    
    def request_access(
        self,
        request_data: PetClinicAccessRequest,
        current_user: User
    ) -> dict:
        """
        Request clinic access (generates OTP and sends to pet owner).
        
        Args:
            request_data: Access request data
            current_user: User requesting access (clinic/doctor)
            
        Returns:
            Dictionary with OTP ID and expiration info
        """
        # Verify pet exists
        pet = self.pet_repository.get_by_id(request_data.pet_id)
        if not pet:
            raise ValueError("Pet not found")
        
        # Verify current user is clinic owner or doctor
        # (In production, also verify they're associated with the clinic)
        
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Create OTP record
        otp = OTP(
            phone_number=current_user.phone or "",  # Should get owner's phone in production
            otp_code=otp_code,
            purpose=OTPPurpose.PET_ACCESS,
            expires_at=datetime.utcnow() + timedelta(minutes=10),
            is_used=False
        )
        self.session.add(otp)
        self.session.commit()
        self.session.refresh(otp)
        
        # TODO: Send OTP to pet owner via SMS/email
        # For now, return OTP in response (DEV ONLY)
        
        return {
            "otp_id": str(otp.id),
            "message": "OTP sent to pet owner",
            "expires_in_minutes": 10,
            # DEV ONLY - remove in production
            "otp_code": otp_code
        }
    
    def grant_access(
        self,
        grant_data: PetClinicAccessGrant,
        current_user: User
    ) -> PetClinicAccess:
        """
        Grant clinic access after OTP validation.
        
        Args:
            grant_data: Access grant data with OTP
            current_user: Pet owner granting access
            
        Returns:
            PetClinicAccess instance
        """
        # Verify pet belongs to current user
        pet = self.pet_repository.get_by_id(grant_data.pet_id)
        if not pet:
            raise ValueError("Pet not found")
        
        if str(pet.owner_id) != str(current_user.public_id):
            raise PermissionError("You can only grant access to your own pets")
        
        # Validate OTP
        otp = self.session.query(OTP).filter(
            OTP.otp_code == grant_data.otp_code,
            OTP.purpose == OTPPurpose.PET_ACCESS,
            OTP.is_used == False
        ).first()
        
        if not otp:
            raise ValueError("Invalid OTP code")
        
        if otp.is_expired():
            raise ValueError("OTP has expired")
        
        # Mark OTP as used
        otp.is_used = True
        
        # Convert UUIDs
        try:
            pet_id_uuid = uuid.UUID(grant_data.pet_id)
            clinic_id_uuid = uuid.UUID(grant_data.clinic_id)
            doctor_id_uuid = uuid.UUID(grant_data.doctor_id) if grant_data.doctor_id else None
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        # Calculate expiration
        access_granted_at = datetime.utcnow()
        access_expires_at = access_granted_at + timedelta(hours=grant_data.access_duration_hours)
        
        # Create access record
        access = self.pet_clinic_access_repository.create(
            pet_id=pet_id_uuid,
            clinic_id=clinic_id_uuid,
            doctor_id=doctor_id_uuid,
            owner_id=current_user.public_id,
            access_granted_at=access_granted_at,
            access_expires_at=access_expires_at,
            status=AccessStatus.ACTIVE,
            otp_id=otp.id,
            purpose=grant_data.purpose if hasattr(grant_data, 'purpose') else None
        )
        
        self.session.commit()
        
        return access
    
    def revoke_access(
        self,
        access_id: str,
        current_user: User
    ) -> bool:
        """
        Revoke clinic access to pet records.
        
        Args:
            access_id: Access record ID to revoke
            current_user: Pet owner revoking access
            
        Returns:
            True if revoked, False otherwise
        """
        access = self.pet_clinic_access_repository.get_by_id(access_id)
        
        if not access:
            return False
        
        # Verify current user is the pet owner
        if str(access.owner_id) != str(current_user.public_id):
            raise PermissionError("You can only revoke access you granted")
        
        # Revoke the access
        return self.pet_clinic_access_repository.revoke_access(access_id)
    
    def check_active_access(
        self,
        pet_id: str,
        clinic_id: str
    ) -> Optional[PetClinicAccess]:
        """
        Check if a clinic has active access to a pet.
        
        Args:
            pet_id: Pet's ID
            clinic_id: Clinic's ID
            
        Returns:
            Active PetClinicAccess or None
        """
        return self.pet_clinic_access_repository.get_active_access(pet_id, clinic_id)
    
    def expire_old_access_records(self) -> int:
        """
        Mark expired access records as expired.
        
        This should be run periodically (e.g., via cron job).
        
        Returns:
            Number of records expired
        """
        expired_records = self.pet_clinic_access_repository.get_expired_access()
        
        count = 0
        for record in expired_records:
            record.status = AccessStatus.EXPIRED
            count += 1
        
        if count > 0:
            self.session.commit()
        
        return count

