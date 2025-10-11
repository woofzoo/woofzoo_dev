"""
Pet service for business logic operations.

This module provides the PetService class for pet-related business logic,
acting as an intermediary between controllers and repositories.
"""

import uuid
import secrets
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple
from passlib.context import CryptContext

from app.models.pet import Pet
from app.models.user import User
from app.repositories.pet import PetRepository
from app.repositories.user import UserRepository
from app.services.email import EmailService
from app.schemas.pet import PetCreate, PetUpdate, ClinicPetOnboardingRequest
from app.config import settings
from loguru import logger


class PetService:
    """
    Pet service for business logic operations.
    
    This class handles business logic for pet operations, including
    validation, business rules, and coordination between repositories.
    """
    
    def __init__(
        self, 
        pet_repository: PetRepository, 
        pet_id_service,
        user_repository: Optional[UserRepository] = None,
        email_service: Optional[EmailService] = None
    ) -> None:
        """Initialize the pet service."""
        self.pet_repository = pet_repository
        self.pet_id_service = pet_id_service
        self.user_repository = user_repository
        self.email_service = email_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def create_pet(self, pet_data: PetCreate) -> Pet:
        """Create a new pet with business logic validation."""
        # Convert owner_id string to UUID
        try:
            owner_id_uuid = uuid.UUID(pet_data.owner_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid owner_id format: {pet_data.owner_id}")
        
        # Generate unique pet ID
        pet_id = self.pet_id_service.generate_pet_id(pet_data.pet_type, pet_data.breed)
        
        # Create the pet
        pet = self.pet_repository.create(
            pet_id=pet_id,
            owner_id=owner_id_uuid,
            name=pet_data.name,
            pet_type=pet_data.pet_type,
            breed=pet_data.breed,
            age=pet_data.age,
            gender=pet_data.gender,
            weight=pet_data.weight,
            photos=pet_data.photos or [],
            emergency_contacts=pet_data.emergency_contacts or {},
            insurance_info=pet_data.insurance_info or {}
        )
        
        return pet
    
    def get_pet_by_id(self, pet_id: str) -> Optional[Pet]:
        """Get a pet by ID."""
        return self.pet_repository.get_by_id(pet_id)
    
    def get_pet_by_pet_id(self, pet_id: str) -> Optional[Pet]:
        """Get a pet by pet_id."""
        return self.pet_repository.get_by_pet_id(pet_id)
    
    def get_pets_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Get all pets for a specific owner."""
        return self.pet_repository.get_by_owner_id(owner_id, skip=skip, limit=limit)
    
    def update_pet(self, pet_id: str, pet_data: PetUpdate) -> Optional[Pet]:
        """Update a pet with business logic validation."""
        # Check if pet exists
        existing_pet = self.pet_repository.get_by_id(pet_id)
        if not existing_pet:
            return None
        
        # Prepare update data
        update_data = {}
        if pet_data.name is not None:
            update_data["name"] = pet_data.name
        if pet_data.pet_type is not None:
            update_data["pet_type"] = pet_data.pet_type
        if pet_data.breed is not None:
            update_data["breed"] = pet_data.breed
        if pet_data.age is not None:
            update_data["age"] = pet_data.age
        if pet_data.gender is not None:
            update_data["gender"] = pet_data.gender
        if pet_data.weight is not None:
            update_data["weight"] = pet_data.weight
        if pet_data.photos is not None:
            update_data["photos"] = pet_data.photos
        if pet_data.emergency_contacts is not None:
            update_data["emergency_contacts"] = pet_data.emergency_contacts
        if pet_data.insurance_info is not None:
            update_data["insurance_info"] = pet_data.insurance_info
        
        # Update the pet
        return self.pet_repository.update(pet_id, **update_data)
    
    def delete_pet(self, pet_id: str) -> bool:
        """Delete a pet (soft delete)."""
        return self.pet_repository.delete(pet_id)
    
    def search_pets(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Search pets by name or breed."""
        if not search_term.strip():
            return self.pet_repository.get_all(skip=skip, limit=limit)
        
        return self.pet_repository.search_pets(
            search_term=search_term.strip(),
            skip=skip,
            limit=limit
        )
    
    def get_pets_by_type(self, pet_type: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Get pets by type."""
        return self.pet_repository.get_by_pet_type(pet_type, skip=skip, limit=limit)
    
    def get_pets_by_breed(self, breed: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Get pets by breed."""
        return self.pet_repository.get_by_breed(breed, skip=skip, limit=limit)
    
    def count_pets_by_owner(self, owner_id: str) -> int:
        """Count pets for a specific owner."""
        return self.pet_repository.count_by_owner(owner_id)
    
    def count_active_pets(self) -> int:
        """Count all active pets."""
        return self.pet_repository.count_active_pets()
    
    def lookup_pet(self, pet_id: str) -> Optional[Pet]:
        """Lookup a pet by pet_id."""
        return self.pet_repository.get_by_pet_id(pet_id)
    
    def onboard_pet_by_clinic(
        self, 
        onboarding_data: ClinicPetOnboardingRequest,
        clinic_user_id: uuid.UUID
    ) -> Tuple[Pet, User, bool]:
        """
        Onboard a pet via clinic. Creates user if needed and sends notification email.
        
        Args:
            onboarding_data: Clinic pet onboarding request data
            clinic_user_id: UUID of the clinic user performing onboarding
            
        Returns:
            Tuple[Pet, User, bool]: (created pet, owner user, is_new_user)
            
        Raises:
            ValueError: If validation fails or dependencies not available
        """
        if not self.user_repository:
            raise ValueError("User repository not available for clinic onboarding")
        if not self.email_service:
            raise ValueError("Email service not available for clinic onboarding")
        
        # 1. Check if user exists by email
        existing_user = self.user_repository.get_by_email(onboarding_data.owner_email)
        is_new_user = False
        verification_token = None
        
        if existing_user:
            # User already exists
            owner_user = existing_user
            logger.info(
                "Using existing user for pet onboarding",
                extra={"user_email": onboarding_data.owner_email, "user_id": str(owner_user.public_id)}
            )
        else:
            # 2. Create new user account
            is_new_user = True
            
            # Generate random password
            random_password = secrets.token_urlsafe(16)
            hashed_password = self.pwd_context.hash(random_password)
            
            # Generate verification token
            verification_token = secrets.token_urlsafe(32)
            verification_expires = datetime.now(timezone.utc) + timedelta(hours=settings.email_verification_expire_hours)
            
            # Parse name into first and last name
            if onboarding_data.owner_name:
                name_parts = onboarding_data.owner_name.strip().split(maxsplit=1)
                first_name = name_parts[0] if len(name_parts) > 0 else "Pet"
                last_name = name_parts[1] if len(name_parts) > 1 else "Owner"
            else:
                first_name = "Pet"
                last_name = "Owner"
            
            # Create user with pet_owner role
            owner_user = self.user_repository.create(
                email=onboarding_data.owner_email,
                password_hash=hashed_password,
                first_name=first_name,
                last_name=last_name,
                phone=onboarding_data.owner_phone,
                roles=["pet_owner"],
                email_verification_token=verification_token,
                email_verification_expires=verification_expires,
                personalization={},
                is_verified=False  # Require email verification
            )
            
            logger.info(
                "Created new user for pet onboarding",
                extra={
                    "user_email": onboarding_data.owner_email,
                    "user_id": str(owner_user.public_id),
                    "first_name": first_name,
                    "last_name": last_name
                }
            )
        
        # 3. Generate pet_id
        pet_id = self.pet_id_service.generate_pet_id(
            onboarding_data.pet_type,
            onboarding_data.breed
        )
        
        # 4. Create pet with owner_id = user.public_id
        pet = self.pet_repository.create(
            pet_id=pet_id,
            owner_id=owner_user.public_id,  # This makes the user the admin/owner of the pet
            name=onboarding_data.pet_name,
            pet_type=onboarding_data.pet_type,
            breed=onboarding_data.breed,
            age=onboarding_data.age,
            gender=onboarding_data.gender,
            weight=onboarding_data.weight,
            photos=[],
            emergency_contacts=onboarding_data.emergency_contacts or {},
            insurance_info=onboarding_data.insurance_info or {}
        )
        
        logger.info(
            "Pet created successfully for clinic onboarding",
            extra={
                "pet_id": pet_id,
                "pet_name": onboarding_data.pet_name,
                "owner_id": str(owner_user.public_id),
                "is_new_user": is_new_user
            }
        )
        
        # 5. Send notification email
        try:
            email_sent = self.email_service.send_pet_onboarding_notification_email(
                to_email=owner_user.email,
                to_name=owner_user.full_name,
                pet_name=onboarding_data.pet_name,
                pet_type=onboarding_data.pet_type,
                pet_breed=onboarding_data.breed,
                clinic_name="Clinic",  # TODO: Get actual clinic name from clinic_user_id
                is_new_user=is_new_user,
                verification_token=verification_token
            )
            
            if email_sent:
                logger.info(
                    "Pet onboarding notification email sent",
                    extra={"recipient_email": owner_user.email, "pet_id": pet_id}
                )
            else:
                logger.warning(
                    "Failed to send pet onboarding notification email",
                    extra={"recipient_email": owner_user.email, "pet_id": pet_id}
                )
        except Exception as e:
            logger.exception(
                "Error sending pet onboarding notification email",
                extra={"recipient_email": owner_user.email, "pet_id": pet_id, "error": str(e)}
            )
        
        # 6. Return results
        return pet, owner_user, is_new_user

