"""
Doctor routes for doctor-specific operations.

This module defines API endpoints for doctor queue management including
viewing queue, pet visit details, updating visits, and completing visits.
"""

from fastapi import APIRouter, Depends, status

from app.models.user import User
from app.dependencies import get_doctor_user
from app.controllers.doctor_controller import DoctorController
from app.schemas.doctor_queue import (
    DoctorQueueResponse,
    PetVisitDetails,
    VisitUpdateRequest,
    VisitUpdateResponse,
    CompleteVisitRequest,
    CompleteVisitResponse,
)


# Router for doctor endpoints
router = APIRouter(
    prefix="/doctor",
    tags=["Doctor Queue"],
    responses={401: {"description": "Not authenticated"}},
)


# Import controller dependency
from app.dependencies import get_doctor_controller


@router.get(
    "/queue/today",
    response_model=DoctorQueueResponse,
    status_code=status.HTTP_200_OK,
    summary="Get today's queue (doctor only)",
    description="Get all pets assigned to the doctor for today with visit information."
)
def get_todays_queue(
    current_user: User = Depends(get_doctor_user),
    controller: DoctorController = Depends(get_doctor_controller)
) -> DoctorQueueResponse:
    """
    Get today's queue for the logged-in doctor.
    
    **Authorization**: Requires `doctor` role.
    
    **Returns**:
    - List of pets in queue with visit information
    - Pre-check vitals for each pet
    - Queue statistics (total, completed, in_progress)
    - Queue position for each pet
    
    **Queue Items Include**:
    - Pet details (name, type, breed, owner)
    - Visit information (type, complaint, assigned time)
    - Pre-check vitals (weight, temperature, heart rate)
    - Current status (with_doctor, completed)
    """
    return controller.get_todays_queue(current_user)


@router.get(
    "/visits/{medical_record_id}",
    response_model=PetVisitDetails,
    status_code=status.HTTP_200_OK,
    summary="Get visit details (doctor only)",
    description="Get detailed information for a specific visit including pet details and medical history."
)
def get_visit_details(
    medical_record_id: str,
    current_user: User = Depends(get_doctor_user),
    controller: DoctorController = Depends(get_doctor_controller)
) -> PetVisitDetails:
    """
    Get detailed information for a specific visit.
    
    **Authorization**: Requires `doctor` role.
    
    **Returns**:
    - Full pet details (name, type, age, weight, owner info)
    - Current visit details (type, complaint, diagnosis, treatment)
    - Medical history (past 10 visits)
    - Known allergies
    - Vaccination history
    
    **Security**: Doctor can only access visits assigned to them.
    """
    return controller.get_visit_details(medical_record_id, current_user)


@router.patch(
    "/visits/{medical_record_id}",
    response_model=VisitUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Update visit details (doctor only)",
    description="Update diagnosis, treatment plan, clinical notes, and vital signs for a visit."
)
def update_visit(
    medical_record_id: str,
    update_data: VisitUpdateRequest,
    current_user: User = Depends(get_doctor_user),
    controller: DoctorController = Depends(get_doctor_controller)
) -> VisitUpdateResponse:
    """
    Update visit details.
    
    **Authorization**: Requires `doctor` role.
    
    **Updatable Fields**:
    - Diagnosis
    - Treatment plan
    - Clinical notes
    - Weight (kg)
    - Temperature (°C)
    - Vital signs (heart rate, respiratory rate, etc.)
    
    **All fields are optional** - only provided fields will be updated.
    
    **Security**: Doctor can only update their own visits.
    """
    return controller.update_visit(medical_record_id, update_data, current_user)


@router.post(
    "/visits/{medical_record_id}/complete",
    response_model=CompleteVisitResponse,
    status_code=status.HTTP_200_OK,
    summary="Complete visit (doctor only)",
    description="Mark a visit as complete and remove from active queue."
)
def complete_visit(
    medical_record_id: str,
    complete_data: CompleteVisitRequest,
    current_user: User = Depends(get_doctor_user),
    controller: DoctorController = Depends(get_doctor_controller)
) -> CompleteVisitResponse:
    """
    Mark visit as complete.
    
    **Authorization**: Requires `doctor` role.
    
    **Process**:
    1. Updates medical record with follow-up info (if provided)
    2. Updates queue status to `completed`
    3. Records completion timestamp
    4. Removes pet from active queue
    5. Visit history becomes available to owner
    
    **Follow-up Options**:
    - Set follow_up_required: true/false
    - Specify follow_up_date
    - Add follow_up_notes (instructions for owner)
    
    **Security**: Doctor can only complete their own visits.
    """
    return controller.complete_visit(medical_record_id, complete_data, current_user)

