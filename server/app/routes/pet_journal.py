"""
Pet Journal routes for API endpoints.

This module defines all pet journal-related API endpoints with proper
dependency injection and request/response handling.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controllers.pet_journal_controller import PetJournalController
from app.database import get_db_session
from app.dependencies import get_current_user_id
from app.schemas.pet_journal import (
    PetJournalCreate,
    PetJournalUpdate,
    PetJournalResponse,
    PetJournalListResponse
)


# Create router
router = APIRouter(prefix="/pets", tags=["pet-journal"])


# Dependency to get pet journal controller
def get_pet_journal_controller(
    db: Session = Depends(get_db_session)
) -> PetJournalController:
    """Get pet journal controller with dependency injection."""
    from app.repositories.pet_journal_repository import PetJournalRepository
    from app.repositories.pet import PetRepository
    from app.services.pet_journal_service import PetJournalService
    
    journal_repo = PetJournalRepository(db)
    pet_repo = PetRepository(db)
    journal_service = PetJournalService(journal_repo, pet_repo)
    return PetJournalController(journal_service)


# API Endpoints
@router.post(
    "/{pet_id}/journal",
    response_model=PetJournalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a pet journal entry",
    description="Create a new journal entry for a pet (activity, medication, event, or health note)"
)
def create_journal_entry(
    journal_data: PetJournalCreate,
    user_id: int = Depends(get_current_user_id),
    controller: PetJournalController = Depends(get_pet_journal_controller)
) -> PetJournalResponse:
    """
    Create a new journal entry for a pet.
    
    Entry types:
    - daily_activity: Daily activities and behaviors
    - medication_given: Medication administration notes
    - activity_event: Special events or activities
    - health_note: Health observations and notes
    """
    return controller.create_journal_entry(journal_data, user_id)


@router.get(
    "/{pet_id}/journal",
    response_model=PetJournalListResponse,
    summary="Get pet journal entries",
    description="Retrieve all journal entries for a pet with optional filtering"
)
def get_journal_entries(
    pet_id: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    entry_type: Optional[str] = Query(default=None, description="Filter by entry type"),
    user_id: int = Depends(get_current_user_id),
    controller: PetJournalController = Depends(get_pet_journal_controller)
) -> PetJournalListResponse:
    """Get all journal entries for a pet with optional filtering by entry type."""
    return controller.get_journal_entries_by_pet(pet_id, skip, limit, entry_type)


@router.get(
    "/{pet_id}/journal/date-range",
    response_model=PetJournalListResponse,
    summary="Get journal entries by date range",
    description="Retrieve journal entries within a specific date range"
)
def get_journal_entries_by_date_range(
    pet_id: str,
    start_date: date = Query(..., description="Start date (inclusive)"),
    end_date: date = Query(..., description="End date (inclusive)"),
    entry_type: Optional[str] = Query(default=None, description="Filter by entry type"),
    user_id: int = Depends(get_current_user_id),
    controller: PetJournalController = Depends(get_pet_journal_controller)
) -> PetJournalListResponse:
    """Get journal entries within a date range."""
    return controller.get_journal_entries_by_date_range(pet_id, start_date, end_date, entry_type)


@router.get(
    "/{pet_id}/journal/{entry_id}",
    response_model=PetJournalResponse,
    summary="Get a specific journal entry",
    description="Retrieve a specific journal entry by ID"
)
def get_journal_entry(
    pet_id: str,
    entry_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: PetJournalController = Depends(get_pet_journal_controller)
) -> PetJournalResponse:
    """Get a specific journal entry by ID."""
    return controller.get_journal_entry(entry_id)


@router.put(
    "/{pet_id}/journal/{entry_id}",
    response_model=PetJournalResponse,
    summary="Update a journal entry",
    description="Update an existing journal entry"
)
def update_journal_entry(
    pet_id: str,
    entry_id: str,
    update_data: PetJournalUpdate,
    user_id: int = Depends(get_current_user_id),
    controller: PetJournalController = Depends(get_pet_journal_controller)
) -> PetJournalResponse:
    """Update an existing journal entry."""
    return controller.update_journal_entry(entry_id, update_data, user_id)


@router.delete(
    "/{pet_id}/journal/{entry_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a journal entry",
    description="Delete an existing journal entry"
)
def delete_journal_entry(
    pet_id: str,
    entry_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: PetJournalController = Depends(get_pet_journal_controller)
) -> dict:
    """Delete a journal entry."""
    return controller.delete_journal_entry(entry_id, user_id)


# Health check endpoint
@router.get(
    "/journal/health",
    summary="Pet Journal service health check",
    description="Check if pet journal service is running"
)
async def health_check() -> dict:
    """Health check endpoint."""
    return {"message": "Pet Journal service is running"}

