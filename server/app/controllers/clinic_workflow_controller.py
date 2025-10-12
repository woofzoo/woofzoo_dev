"""
Clinic Workflow Controller for handling HTTP requests.

This controller manages clinic workflow operations including pet search,
OTP verification, pre-checks, and doctor assignment.
"""

import uuid
from typing import Optional

from fastapi import HTTPException, status

from app.models.user import User
from app.services.clinic_workflow_service import ClinicWorkflowService
from app.schemas.clinic_workflow import (
    PetSearchRequest,
    PetSearchResponse,
    PetBasicInfo,
    OwnerBasicInfo,
    OTPRequestData,
    OTPRequestResponse,
    OTPVerifyRequest,
    OTPVerifyResponse,
    PreCheckVitalsUpdate,
    PreCheckVitalsResponse,
    AssignDoctorRequest,
    AssignDoctorResponse,
)
from app.logger import logger


class ClinicWorkflowController:
    """Controller for clinic workflow operations."""
    
    def __init__(self, clinic_workflow_service: ClinicWorkflowService):
        """Initialize the clinic workflow controller."""
        self.clinic_workflow_service = clinic_workflow_service
    
    def search_pet(
        self,
        search_request: PetSearchRequest,
        current_user: User
    ) -> PetSearchResponse:
        """
        Search for a pet by owner email, phone, or pet_id.
        
        Args:
            search_request: Pet search request
            current_user: Current authenticated clinic user
            
        Returns:
            PetSearchResponse: Search results
            
        Raises:
            HTTPException: If search fails
        """
        try:
            logger.info(
                "Pet search request received",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "search_type": search_request.search_type,
                }
            )
            
            result = self.clinic_workflow_service.search_pet(
                search_type=search_request.search_type,
                search_value=search_request.search_value,
                clinic_user_id=current_user.public_id
            )
            
            if result:
                pet, owner = result
                
                # Build response
                return PetSearchResponse(
                    found=True,
                    pet=PetBasicInfo(
                        id=str(pet.id),
                        pet_id=pet.pet_id,
                        name=pet.name,
                        pet_type=pet.pet_type,
                        breed=pet.breed,
                        age=pet.age,
                        gender=pet.gender,
                        owner=OwnerBasicInfo(
                            id=str(owner.public_id),
                            name=owner.full_name,
                            email=owner.email,
                            phone=owner.phone
                        )
                    )
                )
            else:
                return PetSearchResponse(
                    found=False,
                    message=f"No pet found with {search_request.search_type}: {search_request.search_value}"
                )
        
        except ValueError as e:
            logger.warning(
                "Pet search validation error",
                extra={"clinic_user_id": str(current_user.id), "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Pet search failed",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "search_type": search_request.search_type
                }
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search for pet"
            )
    
    def request_otp(
        self,
        otp_request: OTPRequestData,
        current_user: User
    ) -> OTPRequestResponse:
        """
        Request OTP for clinic visit access.
        
        Args:
            otp_request: OTP request data
            current_user: Current authenticated clinic user
            
        Returns:
            OTPRequestResponse: OTP request response
            
        Raises:
            HTTPException: If OTP request fails
        """
        try:
            pet_id = uuid.UUID(otp_request.pet_id)
            
            # TODO: Get actual clinic_id from current_user's clinic profile
            # For now, using a placeholder
            clinic_id = current_user.public_id  # This should be clinic profile ID
            
            logger.info(
                "OTP request initiated",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "pet_id": str(pet_id)
                }
            )
            
            otp, owner_email = self.clinic_workflow_service.request_otp_for_visit(
                pet_id=pet_id,
                clinic_id=clinic_id,
                clinic_user_id=current_user.public_id,
                purpose=otp_request.purpose
            )
            
            # In development, include OTP code in response
            # TODO: Remove in production
            import os
            include_otp = os.getenv("ENVIRONMENT", "development") == "development"
            
            return OTPRequestResponse(
                otp_id=str(otp.id),
                message="OTP sent to pet owner's email",
                owner_email=owner_email,
                expires_in_minutes=10,
                otp_code=otp.otp_code if include_otp else None
            )
        
        except ValueError as e:
            logger.warning(
                "OTP request validation error",
                extra={"clinic_user_id": str(current_user.id), "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "OTP request failed",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "pet_id": otp_request.pet_id
                }
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to request OTP"
            )
    
    def verify_otp(
        self,
        verify_request: OTPVerifyRequest,
        current_user: User
    ) -> OTPVerifyResponse:
        """
        Verify OTP and create clinic access record.
        
        Args:
            verify_request: OTP verification request
            current_user: Current authenticated clinic user
            
        Returns:
            OTPVerifyResponse: OTP verification response
            
        Raises:
            HTTPException: If OTP verification fails
        """
        try:
            pet_id = uuid.UUID(verify_request.pet_id)
            
            # TODO: Get actual clinic_id from current_user's clinic profile
            clinic_id = current_user.public_id
            
            logger.info(
                "OTP verification initiated",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "pet_id": str(pet_id)
                }
            )
            
            access = self.clinic_workflow_service.verify_otp_and_create_access(
                pet_id=pet_id,
                clinic_id=clinic_id,
                otp_code=verify_request.otp_code,
                clinic_user_id=current_user.public_id
            )
            
            return OTPVerifyResponse(
                success=True,
                message="OTP verified successfully. Pet ready for pre-checks.",
                access_record_id=str(access.id),
                queue_status=access.queue_status
            )
        
        except ValueError as e:
            logger.warning(
                "OTP verification failed",
                extra={"clinic_user_id": str(current_user.id), "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "OTP verification error",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "pet_id": verify_request.pet_id
                }
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to verify OTP"
            )
    
    def update_pre_checks(
        self,
        access_record_id: str,
        pre_check_data: PreCheckVitalsUpdate,
        current_user: User
    ) -> PreCheckVitalsResponse:
        """
        Update pre-check vitals for a pet.
        
        Args:
            access_record_id: Access record ID
            pre_check_data: Pre-check vitals data
            current_user: Current authenticated clinic user
            
        Returns:
            PreCheckVitalsResponse: Pre-check update response
            
        Raises:
            HTTPException: If pre-check update fails
        """
        try:
            access_id = uuid.UUID(access_record_id)
            
            logger.info(
                "Pre-check vitals update initiated",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "access_record_id": access_record_id
                }
            )
            
            access = self.clinic_workflow_service.update_pre_check_vitals(
                access_record_id=access_id,
                clinic_user_id=current_user.public_id,
                weight=pre_check_data.weight,
                temperature=pre_check_data.temperature,
                heart_rate=pre_check_data.heart_rate,
                respiratory_rate=pre_check_data.respiratory_rate,
                notes=pre_check_data.notes
            )
            
            return PreCheckVitalsResponse(
                success=True,
                message="Pre-check vitals recorded successfully",
                access_record_id=str(access.id),
                queue_status=access.queue_status,
                pre_checks={
                    "weight": access.pre_check_weight,
                    "temperature": access.pre_check_temperature,
                    "heart_rate": access.pre_check_heart_rate,
                    "respiratory_rate": access.pre_check_respiratory_rate,
                    "notes": access.pre_check_notes,
                    "recorded_at": access.pre_check_completed_at.isoformat() if access.pre_check_completed_at else None,
                    "recorded_by": str(access.pre_check_by_user_id) if access.pre_check_by_user_id else None
                }
            )
        
        except ValueError as e:
            logger.warning(
                "Pre-check vitals update validation error",
                extra={"clinic_user_id": str(current_user.id), "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Pre-check vitals update failed",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "access_record_id": access_record_id
                }
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update pre-check vitals"
            )
    
    def assign_to_doctor(
        self,
        access_record_id: str,
        assign_request: AssignDoctorRequest,
        current_user: User
    ) -> AssignDoctorResponse:
        """
        Assign pet to doctor and create medical record.
        
        Args:
            access_record_id: Access record ID
            assign_request: Doctor assignment request
            current_user: Current authenticated clinic user
            
        Returns:
            AssignDoctorResponse: Doctor assignment response
            
        Raises:
            HTTPException: If doctor assignment fails
        """
        try:
            access_id = uuid.UUID(access_record_id)
            doctor_id = uuid.UUID(assign_request.doctor_id)
            
            logger.info(
                "Doctor assignment initiated",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "access_record_id": access_record_id,
                    "doctor_id": str(doctor_id)
                }
            )
            
            access, medical_record = self.clinic_workflow_service.assign_to_doctor(
                access_record_id=access_id,
                clinic_user=current_user,
                doctor_id=doctor_id,
                visit_type=assign_request.visit_type,
                chief_complaint=assign_request.chief_complaint
            )
            
            return AssignDoctorResponse(
                success=True,
                message="Pet assigned to doctor successfully",
                access_record={
                    "id": str(access.id),
                    "pet_id": str(access.pet_id),
                    "doctor_id": str(doctor_id),
                    "queue_status": access.queue_status,
                    "queue_position": access.queue_position
                },
                medical_record={
                    "id": str(medical_record.id),
                    "visit_date": medical_record.visit_date.isoformat()
                }
            )
        
        except ValueError as e:
            logger.warning(
                "Doctor assignment validation error",
                extra={"clinic_user_id": str(current_user.id), "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Doctor assignment failed",
                extra={
                    "clinic_user_id": str(current_user.id),
                    "access_record_id": access_record_id
                }
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to assign pet to doctor"
            )

