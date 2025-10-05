"""
Family Member controller for API layer.

This module provides the FamilyMemberController class for handling HTTP requests
and responses related to family member operations.
"""

from typing import List

from fastapi import HTTPException, status

from app.schemas.family import FamilyMemberCreate, FamilyMemberListResponse, FamilyMemberResponse, FamilyMemberUpdate
from app.services.family_member import FamilyMemberService
from loguru import logger


class FamilyMemberController:
    """
    Family Member controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to family member operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, family_member_service: FamilyMemberService) -> None:
        """Initialize the family member controller."""
        self.family_member_service = family_member_service
    
    def add_family_member(self, family_id: str, member_data: FamilyMemberCreate) -> FamilyMemberResponse:
        """Add a new family member."""
        try:
            member = self.family_member_service.add_family_member(family_id, member_data)
            return FamilyMemberResponse.model_validate(member)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Failed to add family member to family_id={family_id}", family_id=family_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add family member"
            )
    
    def get_family_member(self, member_id: str) -> FamilyMemberResponse:
        """Get a family member by ID."""
        member = self.family_member_service.get_family_member_by_id(member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Family member with ID {member_id} not found"
            )
        
        return FamilyMemberResponse.model_validate(member)
    
    def get_family_members(self, family_id: str, skip: int = 0, limit: int = 100) -> FamilyMemberListResponse:
        """Get family members by family ID with pagination."""
        try:
            members = self.family_member_service.get_family_members(family_id, skip=skip, limit=limit)
            total = self.family_member_service.get_family_member_count(family_id)
            
            member_responses = [FamilyMemberResponse.model_validate(member) for member in members]
            return FamilyMemberListResponse(members=member_responses, total=total)
        except Exception as e:
            logger.exception("Failed to retrieve family members for family_id={family_id}", family_id=family_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve family members"
            )
    
    def get_user_families(self, user_id: str, skip: int = 0, limit: int = 100) -> FamilyMemberListResponse:
        """Get user's family memberships with pagination."""
        try:
            memberships = self.family_member_service.get_user_families(user_id, skip=skip, limit=limit)
            total = self.family_member_service.get_user_family_count(user_id)
            
            membership_responses = [FamilyMemberResponse.model_validate(membership) for membership in memberships]
            return FamilyMemberListResponse(members=membership_responses, total=total)
        except Exception as e:
            logger.exception("Failed to retrieve user families for user_id={user_id}", user_id=user_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve user families"
            )
    
    def update_family_member(self, member_id: str, member_data: FamilyMemberUpdate) -> FamilyMemberResponse:
        """Update a family member."""
        try:
            member = self.family_member_service.update_family_member(member_id, member_data)
            if not member:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Family member with ID {member_id} not found"
                )
            
            return FamilyMemberResponse.model_validate(member)
        except HTTPException as http_exc:
            logger.warning("Update family member failed: {detail}", detail=str(http_exc.detail))
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Failed to update family member id={member_id}", member_id=member_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update family member"
            )
    
    def remove_family_member(self, member_id: str) -> dict:
        """Remove a family member."""
        try:
            deleted = self.family_member_service.remove_family_member(member_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Family member with ID {member_id} not found"
                )
            
            return {"message": f"Family member with ID {member_id} removed successfully"}
        except HTTPException as http_exc:
            logger.warning("Remove family member failed: {detail}", detail=str(http_exc.detail))
            raise
        except Exception as e:
            logger.exception("Failed to remove family member id={member_id}", member_id=member_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove family member"
            )
    
    def remove_user_from_family(self, family_id: str, user_id: str) -> dict:
        """Remove a user from a family."""
        try:
            removed = self.family_member_service.remove_user_from_family(family_id, user_id)
            if not removed:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User is not a member of this family"
                )
            
            return {"message": f"User removed from family successfully"}
        except HTTPException as http_exc:
            logger.warning("Remove user from family failed: {detail}", detail=str(http_exc.detail))
            raise
        except Exception as e:
            logger.exception("Failed to remove user_id={user_id} from family_id={family_id}", user_id=user_id, family_id=family_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove user from family"
            )
