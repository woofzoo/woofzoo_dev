"""
Clinic Workflow routes for clinic operations.

This module defines API endpoints for clinic workflow operations including
pet search, OTP verification, pre-checks, and doctor assignment.
"""

from fastapi import APIRouter, Depends, status

from app.models.user import User
from app.dependencies import get_clinic_owner_user
from app.controllers.clinic_workflow_controller import ClinicWorkflowController
from app.schemas.clinic_workflow import (
    PetSearchRequest,
    PetSearchResponse,
    OTPRequestData,
    OTPRequestResponse,
    OTPVerifyRequest,
    OTPVerifyResponse,
    PreCheckVitalsUpdate,
    PreCheckVitalsResponse,
    AssignDoctorRequest,
    AssignDoctorResponse,
)


# Router for clinic workflow endpoints
router = APIRouter(
    prefix="/clinic",
    tags=["Clinic Workflow"],
    responses={401: {"description": "Not authenticated"}},
)


# Import controller dependency
from app.dependencies import get_clinic_workflow_controller


@router.post(
    "/pets/search",
    response_model=PetSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search for a pet (clinic_owner only)",
    description="Search for a pet by owner email, phone, or pet_id. Returns basic pet and owner information."
)
def search_pet(
    search_request: PetSearchRequest,
    current_user: User = Depends(get_clinic_owner_user),
    controller: ClinicWorkflowController = Depends(get_clinic_workflow_controller)
) -> PetSearchResponse:
    """
    Search for a pet by owner email, phone, or pet_id.
    
    **Authorization**: Requires `clinic_owner` role.
    
    **Search Types**:
    - `email`: Search by pet owner's email address
    - `phone`: Search by pet owner's phone number
    - `pet_id`: Search by pet's ID (e.g., DOG-GOLDEN-RETRIEVER-000001)
    
    **Response**:
    - If found: Returns basic pet details and owner information
    - If not found: Returns `found: false` with message
    """
    return controller.search_pet(search_request, current_user)


@router.post(
    "/access/request-otp",
    response_model=OTPRequestResponse,
    status_code=status.HTTP_200_OK,
    summary="Request OTP for clinic visit (clinic_owner only)",
    description="Request OTP to be sent to pet owner's email for clinic visit authorization."
)
def request_otp(
    otp_request: OTPRequestData,
    current_user: User = Depends(get_clinic_owner_user),
    controller: ClinicWorkflowController = Depends(get_clinic_workflow_controller)
) -> OTPRequestResponse:
    """
    Request OTP for clinic visit authorization.
    
    **Authorization**: Requires `clinic_owner` role.
    
    **Process**:
    1. Validates pet exists and user is owner
    2. Generates 6-digit OTP code
    3. Sends OTP to pet owner's email
    4. OTP valid for 10 minutes
    
    **Development Mode**: OTP code included in response for testing.
    **Production Mode**: OTP code not included in response (sent via email only).
    """
    return controller.request_otp(otp_request, current_user)


@router.post(
    "/access/verify-otp",
    response_model=OTPVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify OTP and create access record (clinic_owner only)",
    description="Verify OTP code and create clinic access record. Pet becomes ready for pre-checks."
)
def verify_otp(
    verify_request: OTPVerifyRequest,
    current_user: User = Depends(get_clinic_owner_user),
    controller: ClinicWorkflowController = Depends(get_clinic_workflow_controller)
) -> OTPVerifyResponse:
    """
    Verify OTP and create clinic access record.
    
    **Authorization**: Requires `clinic_owner` role.
    
    **Process**:
    1. Validates OTP code
    2. Checks OTP not expired or used
    3. Creates clinic access record
    4. Sets queue status to `pending_precheck`
    5. Marks OTP as used
    
    **Next Step**: Update pre-check vitals using the returned `access_record_id`.
    """
    return controller.verify_otp(verify_request, current_user)


@router.patch(
    "/access/{access_record_id}/pre-checks",
    response_model=PreCheckVitalsResponse,
    status_code=status.HTTP_200_OK,
    summary="Update pre-check vitals (clinic_owner only)",
    description="Record pre-check vitals for a pet before assigning to doctor."
)
def update_pre_checks(
    access_record_id: str,
    pre_check_data: PreCheckVitalsUpdate,
    current_user: User = Depends(get_clinic_owner_user),
    controller: ClinicWorkflowController = Depends(get_clinic_workflow_controller)
) -> PreCheckVitalsResponse:
    """
    Update pre-check vitals for a pet.
    
    **Authorization**: Requires `clinic_owner` role.
    
    **Pre-Check Vitals** (all optional):
    - Weight (kg)
    - Temperature (°C)
    - Heart rate (BPM)
    - Respiratory rate (breaths per minute)
    - Notes (observations)
    
    **Process**:
    1. Validates access record exists and status is `pending_precheck`
    2. Records vital signs
    3. Updates queue status to `ready_for_doctor`
    4. Records timestamp and staff member
    
    **Next Step**: Assign pet to doctor using the same `access_record_id`.
    """
    return controller.update_pre_checks(access_record_id, pre_check_data, current_user)


@router.post(
    "/access/{access_record_id}/assign-doctor",
    response_model=AssignDoctorResponse,
    status_code=status.HTTP_200_OK,
    summary="Assign pet to doctor (clinic_owner only)",
    description="Assign pet to a doctor and create medical record."
)
def assign_to_doctor(
    access_record_id: str,
    assign_request: AssignDoctorRequest,
    current_user: User = Depends(get_clinic_owner_user),
    controller: ClinicWorkflowController = Depends(get_clinic_workflow_controller)
) -> AssignDoctorResponse:
    """
    Assign pet to doctor and create medical record.
    
    **Authorization**: Requires `clinic_owner` role.
    
    **Process**:
    1. Validates access record exists and status is `ready_for_doctor`
    2. Creates medical record with visit details
    3. Links pre-check vitals to medical record
    4. Updates queue status to `with_doctor`
    5. Assigns queue position
    6. Records assignment timestamp
    
    **Result**: Pet appears in doctor's queue and medical record is ready for updates.
    """
    return controller.assign_to_doctor(access_record_id, assign_request, current_user)

