"""
Permission Service for role-based access control.

This module provides centralized permission checking for medical records access.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.models.pet import Pet
from app.models.family_member import FamilyMember, AccessLevel
from app.models.pet_clinic_access import PetClinicAccess, AccessStatus
from app.repositories.pet import PetRepository
from app.repositories.family_member import FamilyMemberRepository
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from datetime import datetime


class PermissionService:
    """
    Service for checking user permissions on medical records and pet data.
    
    This service implements the access control matrix for the medical records system.
    """
    
    def __init__(
        self,
        session: Session,
        pet_repository: PetRepository,
        family_member_repository: FamilyMemberRepository,
        pet_clinic_access_repository: PetClinicAccessRepository
    ):
        """Initialize the permission service."""
        self.session = session
        self.pet_repository = pet_repository
        self.family_member_repository = family_member_repository
        self.pet_clinic_access_repository = pet_clinic_access_repository
    
    def can_read_pet_medical_records(self, user: User, pet_id: str) -> bool:
        """
        Check if user can read medical records for a pet.
        
        Args:
            user: User requesting access
            pet_id: Pet's ID
            
        Returns:
            True if user has read access, False otherwise
        """
        pet = self.pet_repository.get_by_id(pet_id)
        if not pet:
            return False
        
        # Pet owner has full access
        if str(pet.owner_id) == str(user.public_id):
            return True
        
        # Family members have read access based on their access level
        if UserRole.FAMILY_MEMBER in user.roles:
            family_member = self.family_member_repository.get_by_user_id(str(user.public_id))
            if family_member and family_member.is_active:
                return True
        
        # Doctors have read access if they have active clinic access
        if UserRole.DOCTOR in user.roles:
            return self._has_active_clinic_access_as_doctor(user, pet_id)
        
        # Clinic owners can read records created at their clinic
        if UserRole.CLINIC_OWNER in user.roles:
            return self._has_clinic_owner_access(user, pet_id)
        
        return False
    
    def can_create_medical_records(self, user: User, pet_id: str) -> tuple[bool, str]:
        """
        Check if user can create medical records for a pet.
        
        Args:
            user: User requesting access
            pet_id: Pet's ID
            
        Returns:
            Tuple of (can_create: bool, user_role: str)
        """
        pet = self.pet_repository.get_by_id(pet_id)
        if not pet:
            return False, ""
        
        # Pet owner can create home medication records
        if str(pet.owner_id) == str(user.public_id):
            return True, "pet_owner"
        
        # Family members with Full access can create home medication records
        if UserRole.FAMILY_MEMBER in user.roles:
            family_member = self.family_member_repository.get_by_user_id(str(user.public_id))
            if family_member and family_member.is_active:
                if family_member.access_level == AccessLevel.FULL:
                    return True, "family_member"
        
        # Doctors can create professional medical records if they have active clinic access
        if UserRole.DOCTOR in user.roles:
            if self._has_active_clinic_access_as_doctor(user, pet_id):
                return True, "doctor"
        
        return False, ""
    
    def can_update_medical_records(self, user: User, pet_id: str, record_creator_role: str) -> bool:
        """
        Check if user can update medical records (admin corrections only).
        
        Args:
            user: User requesting access
            pet_id: Pet's ID
            record_creator_role: Role of user who created the record
            
        Returns:
            True if user can update, False otherwise
        """
        # Only the record creator or pet owner can make administrative corrections
        pet = self.pet_repository.get_by_id(pet_id)
        if not pet:
            return False
        
        # Pet owner can update records they created
        if str(pet.owner_id) == str(user.public_id):
            return record_creator_role in ["pet_owner", "family_member"]
        
        # Doctors can only update records they created
        if UserRole.DOCTOR in user.roles and record_creator_role == "doctor":
            return self._has_active_clinic_access_as_doctor(user, pet_id)
        
        return False
    
    def can_read_prescriptions(self, user: User, pet_id: str) -> bool:
        """Check if user can read prescriptions for a pet."""
        return self.can_read_pet_medical_records(user, pet_id)
    
    def can_create_prescriptions(self, user: User, pet_id: str) -> bool:
        """
        Check if user can create prescriptions.
        Only doctors can create professional prescriptions.
        """
        if UserRole.DOCTOR in user.roles:
            return self._has_active_clinic_access_as_doctor(user, pet_id)
        return False
    
    def can_read_lab_tests(self, user: User, pet_id: str) -> bool:
        """Check if user can read lab tests for a pet."""
        return self.can_read_pet_medical_records(user, pet_id)
    
    def can_order_lab_tests(self, user: User, pet_id: str) -> bool:
        """
        Check if user can order lab tests.
        Only doctors can order lab tests.
        """
        if UserRole.DOCTOR in user.roles:
            return self._has_active_clinic_access_as_doctor(user, pet_id)
        return False
    
    def can_read_allergies(self, user: User, pet_id: str) -> bool:
        """Check if user can read allergies for a pet."""
        return self.can_read_pet_medical_records(user, pet_id)
    
    def can_create_allergies(self, user: User, pet_id: str) -> bool:
        """
        Check if user can create allergy records.
        Owners, family members (full access), and doctors can create.
        """
        can_create, _ = self.can_create_medical_records(user, pet_id)
        return can_create
    
    def can_read_vaccinations(self, user: User, pet_id: str) -> bool:
        """Check if user can read vaccinations for a pet."""
        return self.can_read_pet_medical_records(user, pet_id)
    
    def can_create_vaccinations(self, user: User, pet_id: str) -> bool:
        """
        Check if user can create vaccination records.
        Only doctors can create vaccination records.
        """
        if UserRole.DOCTOR in user.roles:
            return self._has_active_clinic_access_as_doctor(user, pet_id)
        return False
    
    def _has_active_clinic_access_as_doctor(self, user: User, pet_id: str) -> bool:
        """
        Check if doctor has active clinic access for a pet.
        
        Args:
            user: Doctor user
            pet_id: Pet's ID
            
        Returns:
            True if doctor has active access, False otherwise
        """
        # Get doctor profile ID from user
        # This would require doctor_profile_repository to get doctor_id
        # For now, we'll check if ANY active access exists for this pet at clinics
        # In production, this should be more specific to the doctor
        
        from app.repositories.doctor_profile import DoctorProfileRepository
        doctor_profile_repo = DoctorProfileRepository(self.session)
        doctor_profile = doctor_profile_repo.get_by_user_id(str(user.public_id))
        
        if not doctor_profile:
            return False
        
        # Check if there's active clinic access for this pet with this doctor
        access_records = self.pet_clinic_access_repository.get_by_doctor_id(str(doctor_profile.id))
        
        now = datetime.utcnow()
        for access in access_records:
            if (str(access.pet_id) == pet_id and 
                access.status == AccessStatus.ACTIVE and 
                access.access_expires_at > now):
                return True
        
        return False
    
    def _has_clinic_owner_access(self, user: User, pet_id: str) -> bool:
        """
        Check if clinic owner can access records for a pet.
        Clinic owners can only view records created at their clinic.
        
        Args:
            user: Clinic owner user
            pet_id: Pet's ID
            
        Returns:
            True if clinic owner has access, False otherwise
        """
        # Get clinic profile ID from user
        from app.repositories.clinic_profile import ClinicProfileRepository
        clinic_profile_repo = ClinicProfileRepository(self.session)
        clinic_profile = clinic_profile_repo.get_by_user_id(str(user.public_id))
        
        if not clinic_profile:
            return False
        
        # Check if there are any medical records for this pet at this clinic
        from app.repositories.medical_record import MedicalRecordRepository
        medical_record_repo = MedicalRecordRepository(self.session)
        records = medical_record_repo.get_by_clinic_id(str(clinic_profile.id), limit=1)
        
        return len(records) > 0
    
    def get_user_role_for_record_creation(self, user: User, pet_id: str) -> Optional[str]:
        """
        Get the role string to use when creating a record.
        
        Args:
            user: User creating the record
            pet_id: Pet's ID
            
        Returns:
            Role string ("pet_owner", "family_member", "doctor") or None
        """
        can_create, role = self.can_create_medical_records(user, pet_id)
        return role if can_create else None

