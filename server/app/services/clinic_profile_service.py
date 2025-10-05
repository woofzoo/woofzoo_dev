"""
Clinic Profile Service - Business logic for clinic profile management.
"""

from typing import List, Optional
import uuid

from app.repositories.clinic_profile import ClinicProfileRepository
from app.models.clinic_profile import ClinicProfile
from app.models.user import User
from app.schemas.clinic_profile import ClinicProfileCreate, ClinicProfileUpdate


class ClinicProfileService:
    """Service for managing clinic profiles."""
    
    def __init__(self, repository: ClinicProfileRepository):
        self.repository = repository
    
    def create_profile(self, user: User, profile_data: ClinicProfileCreate) -> ClinicProfile:
        """
        Create clinic profile for user.
        
        User must have 'clinic_owner' role.
        User can only have one clinic profile.
        """
        # Check if user has clinic_owner role
        if "clinic_owner" not in user.roles:
            raise ValueError("User must have 'clinic_owner' role to create clinic profile")
        
        # Check if profile already exists
        existing = self.repository.get_by_user_id(user.public_id)
        if existing:
            raise ValueError("Clinic profile already exists for this user")
        
        # Check if license number is unique
        existing_license = self.repository.get_by_license_number(profile_data.license_number)
        if existing_license:
            raise ValueError("License number already in use")
        
        # Create profile
        profile = ClinicProfile(
            id=uuid.uuid4(),
            user_id=user.public_id,
            clinic_name=profile_data.clinic_name,
            license_number=profile_data.license_number,
            address=profile_data.address,
            phone=profile_data.phone,
            email=profile_data.email,
            operating_hours=profile_data.operating_hours or {},
            services_offered=profile_data.services_offered or [],
            is_verified=False,  # Requires admin verification
            is_active=True
        )
        
        return self.repository.save(profile)
    
    def get_profile_by_id(self, clinic_id: uuid.UUID) -> Optional[ClinicProfile]:
        """Get clinic profile by ID (public information)."""
        return self.repository.get_by_id(clinic_id)
    
    def get_profile_by_user_id(self, user_id: uuid.UUID) -> Optional[ClinicProfile]:
        """Get clinic profile by user ID."""
        return self.repository.get_by_user_id(user_id)
    
    def update_profile(self, user: User, profile_data: ClinicProfileUpdate) -> ClinicProfile:
        """
        Update clinic owner's own profile.
        
        Only the clinic owner can update their clinic.
        """
        # Get existing profile
        profile = self.repository.get_by_user_id(user.public_id)
        if not profile:
            raise ValueError("Clinic profile not found")
        
        # Update fields
        update_data = profile_data.dict(exclude_unset=True)
        
        # Don't allow updating certain fields via API
        update_data.pop('is_verified', None)  # Only admins can verify
        update_data.pop('user_id', None)  # Cannot change user
        
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        return self.repository.update(profile)
    
    def search_clinics(
        self,
        clinic_name: Optional[str] = None,
        is_verified: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClinicProfile]:
        """
        Search for clinics (public endpoint).
        
        Pet owners can use this to find clinics.
        """
        # Build filters
        filters = {}
        if is_verified is not None:
            filters['is_verified'] = is_verified
        
        # Always filter to active clinics
        filters['is_active'] = True
        
        # Use search method if clinic_name provided
        if clinic_name:
            return self.repository.search_by_name(clinic_name, skip=skip, limit=limit)
        
        return self.repository.find_all(filters, skip=skip, limit=limit)
    
    def deactivate_profile(self, user: User) -> ClinicProfile:
        """Deactivate clinic profile (soft delete)."""
        profile = self.repository.get_by_user_id(user.public_id)
        if not profile:
            raise ValueError("Clinic profile not found")
        
        profile.is_active = False
        return self.repository.update(profile)
    
    def verify_profile(self, clinic_id: uuid.UUID, verified: bool = True) -> ClinicProfile:
        """
        Verify clinic profile (admin only).
        
        This should be called by admin service.
        """
        profile = self.repository.get_by_id(clinic_id)
        if not profile:
            raise ValueError("Clinic profile not found")
        
        profile.is_verified = verified
        return self.repository.update(profile)

