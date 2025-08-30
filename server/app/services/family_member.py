"""
Family Member service for business logic operations.

This module provides the FamilyMemberService class for family member-related business logic,
acting as an intermediary between controllers and repositories.
"""

from typing import List, Optional
import uuid

from app.models.family_member import FamilyMember
from app.repositories.family_member import FamilyMemberRepository
from app.schemas.family import FamilyMemberCreate, FamilyMemberUpdate


class FamilyMemberService:
    """
    Family Member service for business logic operations.
    
    This class handles business logic for family member operations, including
    validation, business rules, and coordination between repositories.
    """
    
    def __init__(self, family_member_repository: FamilyMemberRepository) -> None:
        """Initialize the family member service."""
        self.family_member_repository = family_member_repository
    
    def add_family_member(self, family_id: str, member_data: FamilyMemberCreate) -> FamilyMember:
        """Add a new family member with business logic validation."""
        # Convert IDs to UUID
        try:
            family_id_uuid = uuid.UUID(family_id)
            user_id_uuid = uuid.UUID(member_data.user_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid ID format")
        
        # Check if member already exists
        existing_member = self.family_member_repository.get_by_family_and_user(family_id, member_data.user_id)
        if existing_member:
            raise ValueError(f"User is already a member of this family")
        
        # Create the family member
        member = self.family_member_repository.create(
            family_id=family_id_uuid,
            user_id=user_id_uuid,
            access_level=member_data.access_level
        )
        
        return member
    
    def get_family_member_by_id(self, member_id: str) -> Optional[FamilyMember]:
        """Get a family member by ID."""
        return self.family_member_repository.get_by_id(member_id)
    
    def get_family_members(self, family_id: str, skip: int = 0, limit: int = 100) -> List[FamilyMember]:
        """Get family members by family ID with pagination."""
        return self.family_member_repository.get_by_family_id(family_id, skip=skip, limit=limit)
    
    def get_user_families(self, user_id: str, skip: int = 0, limit: int = 100) -> List[FamilyMember]:
        """Get user's family memberships with pagination."""
        return self.family_member_repository.get_by_user_id(user_id, skip=skip, limit=limit)
    
    def get_family_member(self, family_id: str, user_id: str) -> Optional[FamilyMember]:
        """Get family member by family ID and user ID."""
        return self.family_member_repository.get_by_family_and_user(family_id, user_id)
    
    def update_family_member(self, member_id: str, member_data: FamilyMemberUpdate) -> Optional[FamilyMember]:
        """Update a family member with business logic validation."""
        # Check if member exists
        existing_member = self.family_member_repository.get_by_id(member_id)
        if not existing_member:
            return None
        
        # Update the member
        return self.family_member_repository.update(member_id, access_level=member_data.access_level)
    
    def remove_family_member(self, member_id: str) -> bool:
        """Remove a family member."""
        return self.family_member_repository.delete(member_id)
    
    def remove_user_from_family(self, family_id: str, user_id: str) -> bool:
        """Remove a user from a family."""
        member = self.family_member_repository.get_by_family_and_user(family_id, user_id)
        if not member:
            return False
        
        return self.family_member_repository.delete(str(member.id))
    
    def get_family_member_count(self, family_id: str) -> int:
        """Get family member count by family ID."""
        return self.family_member_repository.count_by_family(family_id)
    
    def get_user_family_count(self, user_id: str) -> int:
        """Get user's family membership count."""
        return self.family_member_repository.count_by_user(user_id)
