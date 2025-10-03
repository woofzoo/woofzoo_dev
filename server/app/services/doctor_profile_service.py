"""
Doctor Profile Service - Business logic for doctor profile management.
"""

from typing import List, Optional
import uuid
from datetime import datetime

from app.repositories.doctor_profile import DoctorProfileRepository
from app.models.doctor_profile import DoctorProfile
from app.models.user import User
from app.schemas.doctor_profile import DoctorProfileCreate, DoctorProfileUpdate


class DoctorProfileService:
    """Service for managing doctor profiles."""
    
    def __init__(self, repository: DoctorProfileRepository):
        self.repository = repository
    
    def create_profile(self, user: User, profile_data: DoctorProfileCreate) -> DoctorProfile:
        """
        Create doctor profile for user.
        
        User must have 'doctor' role.
        User can only have one profile.
        """
        # Check if user has doctor role
        if "doctor" not in user.roles:
            raise ValueError("User must have 'doctor' role to create doctor profile")
        
        # Check if profile already exists
        existing = self.repository.get_by_user_id(user.public_id)
        if existing:
            raise ValueError("Doctor profile already exists for this user")
        
        # Check if license number is unique
        existing_license = self.repository.get_by_license_number(profile_data.license_number)
        if existing_license:
            raise ValueError("License number already in use")
        
        # Create profile
        profile = DoctorProfile(
            id=uuid.uuid4(),
            user_id=user.public_id,
            license_number=profile_data.license_number,
            specialization=profile_data.specialization,
            years_of_experience=profile_data.years_of_experience,
            qualifications=profile_data.qualifications or [],
            bio=profile_data.bio,
            is_verified=False,  # Requires admin verification
            is_active=True
        )
        
        return self.repository.save(profile)
    
    def get_profile_by_id(self, doctor_id: uuid.UUID) -> Optional[DoctorProfile]:
        """Get doctor profile by ID."""
        return self.repository.get_by_id(doctor_id)
    
    def get_profile_by_user_id(self, user_id: uuid.UUID) -> Optional[DoctorProfile]:
        """Get doctor profile by user ID."""
        return self.repository.get_by_user_id(user_id)
    
    def update_profile(self, user: User, profile_data: DoctorProfileUpdate) -> DoctorProfile:
        """
        Update doctor's own profile.
        
        Only the doctor can update their own profile.
        """
        # Get existing profile
        profile = self.repository.get_by_user_id(user.public_id)
        if not profile:
            raise ValueError("Doctor profile not found")
        
        # Update fields
        update_data = profile_data.dict(exclude_unset=True)
        
        # Don't allow updating certain fields via API
        update_data.pop('is_verified', None)  # Only admins can verify
        update_data.pop('user_id', None)  # Cannot change user
        
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        return self.repository.update(profile)
    
    def search_doctors(
        self,
        specialization: Optional[str] = None,
        is_verified: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[DoctorProfile]:
        """
        Search for doctors.
        
        Public endpoint for clinics to find doctors to associate with.
        """
        # Build filters
        filters = {}
        if specialization:
            filters['specialization'] = specialization
        if is_verified is not None:
            filters['is_verified'] = is_verified
        
        # Always filter to active doctors
        filters['is_active'] = True
        
        return self.repository.find_all(filters, skip=skip, limit=limit)
    
    def deactivate_profile(self, user: User) -> DoctorProfile:
        """Deactivate doctor profile (soft delete)."""
        profile = self.repository.get_by_user_id(user.public_id)
        if not profile:
            raise ValueError("Doctor profile not found")
        
        profile.is_active = False
        return self.repository.update(profile)
    
    def verify_profile(self, doctor_id: uuid.UUID, verified: bool = True) -> DoctorProfile:
        """
        Verify doctor profile (admin only).
        
        This should be called by admin service.
        """
        profile = self.repository.get_by_id(doctor_id)
        if not profile:
            raise ValueError("Doctor profile not found")
        
        profile.is_verified = verified
        return self.repository.update(profile)

