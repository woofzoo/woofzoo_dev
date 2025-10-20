"""
Doctor Controller for handling doctor-specific HTTP requests.

This controller manages doctor queue operations including viewing queue,
pet visit details, updating visits, and completing visits.
"""

import uuid
from typing import List
from datetime import date

from fastapi import HTTPException, status

from app.models.user import User
from app.services.doctor_queue_service import DoctorQueueService
from app.schemas.doctor_queue import (
    DoctorQueueResponse,
    DoctorQueueItem,
    PetQueueInfo,
    VisitInfo,
    PetVisitDetails,
    MedicalHistoryItem,
    VisitUpdateRequest,
    VisitUpdateResponse,
    CompleteVisitRequest,
    CompleteVisitResponse,
)
from app.logger import logger


class DoctorController:
    """Controller for doctor operations."""
    
    def __init__(self, doctor_queue_service: DoctorQueueService):
        """Initialize the doctor controller."""
        self.doctor_queue_service = doctor_queue_service
    
    def get_todays_queue(
        self,
        current_user: User
    ) -> DoctorQueueResponse:
        """
        Get today's queue for the logged-in doctor.
        
        This method now uses the service layer for profile resolution and data fetching,
        following clean architecture principles. No direct database access.
        
        Args:
            current_user: Current authenticated doctor user
            
        Returns:
            DoctorQueueResponse: Today's queue with statistics
            
        Raises:
            HTTPException: If fetching queue fails or doctor profile not found
        """
        try:
            logger.info(
                "Fetching today's queue",
                extra={"user_id": str(current_user.public_id)}
            )
            
            # Service layer handles profile resolution and data fetching
            queue_details, statistics = self.doctor_queue_service.get_todays_queue_with_details(
                current_user.public_id
            )
            
            # Build response from service data
            queue_list: List[DoctorQueueItem] = []
            for item in queue_details:
                queue_item = DoctorQueueItem(
                    queue_position=item["queue_position"],
                    pet=PetQueueInfo(**item["pet"]),
                    visit_info=VisitInfo(**item["visit_info"]),
                    status=item["status"]
                )
                queue_list.append(queue_item)
            
            return DoctorQueueResponse(
                date=date.today(),
                queue=queue_list,
                **statistics
            )
        
        except ValueError as e:
            # Profile not found or validation error
            logger.warning(
                "Doctor queue access error",
                extra={"user_id": str(current_user.id), "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to fetch today's queue",
                extra={"user_id": str(current_user.id)}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch today's queue"
            )
    
    def get_visit_details(
        self,
        medical_record_id: str,
        current_user: User
    ) -> PetVisitDetails:
        """
        Get detailed information for a specific visit.
        
        Args:
            medical_record_id: Medical record UUID
            current_user: Current authenticated doctor user
            
        Returns:
            PetVisitDetails: Detailed visit information
            
        Raises:
            HTTPException: If fetching details fails or unauthorized
        """
        try:
            record_id = uuid.UUID(medical_record_id)
            
            # Resolve doctor profile ID using service layer
            doctor_id = self.doctor_queue_service.get_doctor_profile_id(current_user.public_id)
            
            logger.info(
                "Fetching visit details",
                extra={
                    "medical_record_id": medical_record_id,
                    "user_id": str(current_user.public_id),
                    "doctor_profile_id": str(doctor_id)
                }
            )
            
            pet, medical_record, owner, medical_history = \
                self.doctor_queue_service.get_visit_details(record_id, doctor_id)
            
            # Build response
            return PetVisitDetails(
                pet={
                    "id": str(pet.id),
                    "pet_id": pet.pet_id,
                    "name": pet.name,
                    "pet_type": pet.pet_type,
                    "breed": pet.breed,
                    "age": pet.age,
                    "gender": pet.gender,
                    "weight": pet.weight,
                    "owner": {
                        "id": str(owner.public_id),
                        "name": owner.full_name,
                        "email": owner.email,
                        "phone": owner.phone
                    }
                },
                current_visit={
                    "id": str(medical_record.id),
                    "visit_date": medical_record.visit_date.isoformat(),
                    "visit_type": medical_record.visit_type or "GENERAL",
                    "chief_complaint": medical_record.chief_complaint,
                    "diagnosis": medical_record.diagnosis,
                    "treatment_plan": medical_record.treatment_plan,
                    "clinical_notes": medical_record.clinical_notes,
                    "vital_signs": medical_record.vital_signs
                },
                medical_history=[
                    MedicalHistoryItem(
                        id=str(record.id),
                        visit_date=record.visit_date,
                        visit_type=record.visit_type or "GENERAL",
                        diagnosis=record.diagnosis,
                        treatment_plan=record.treatment_plan,
                        doctor_name="Unknown",  # TODO: Fetch doctor name
                        clinic_name="Unknown"  # TODO: Fetch clinic name
                    )
                    for record in medical_history
                ],
                allergies=[],  # TODO: Fetch from allergies repository
                vaccinations=[]  # TODO: Fetch from vaccinations repository
            )
        
        except ValueError as e:
            logger.warning(
                "Visit details access error",
                extra={"medical_record_id": medical_record_id, "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to fetch visit details",
                extra={"medical_record_id": medical_record_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch visit details"
            )
    
    def update_visit(
        self,
        medical_record_id: str,
        update_data: VisitUpdateRequest,
        current_user: User
    ) -> VisitUpdateResponse:
        """
        Update visit details.
        
        Args:
            medical_record_id: Medical record UUID
            update_data: Visit update data
            current_user: Current authenticated doctor user
            
        Returns:
            VisitUpdateResponse: Update confirmation
            
        Raises:
            HTTPException: If update fails or unauthorized
        """
        try:
            record_id = uuid.UUID(medical_record_id)
            
            # Resolve doctor profile ID using service layer
            doctor_id = self.doctor_queue_service.get_doctor_profile_id(current_user.public_id)
            
            logger.info(
                "Updating visit details",
                extra={
                    "medical_record_id": medical_record_id,
                    "user_id": str(current_user.public_id),
                    "doctor_profile_id": str(doctor_id)
                }
            )
            
            medical_record = self.doctor_queue_service.update_visit_details(
                medical_record_id=record_id,
                doctor_id=doctor_id,
                diagnosis=update_data.diagnosis,
                treatment_plan=update_data.treatment_plan,
                clinical_notes=update_data.clinical_notes,
                weight=update_data.weight,
                temperature=update_data.temperature,
                vital_signs=update_data.vital_signs
            )
            
            return VisitUpdateResponse(
                success=True,
                message="Visit details updated successfully",
                medical_record_id=str(medical_record.id)
            )
        
        except ValueError as e:
            logger.warning(
                "Visit update access error",
                extra={"medical_record_id": medical_record_id, "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to update visit",
                extra={"medical_record_id": medical_record_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update visit details"
            )
    
    def complete_visit(
        self,
        medical_record_id: str,
        complete_data: CompleteVisitRequest,
        current_user: User
    ) -> CompleteVisitResponse:
        """
        Mark visit as complete.
        
        Args:
            medical_record_id: Medical record UUID
            complete_data: Completion data
            current_user: Current authenticated doctor user
            
        Returns:
            CompleteVisitResponse: Completion confirmation
            
        Raises:
            HTTPException: If completion fails or unauthorized
        """
        try:
            record_id = uuid.UUID(medical_record_id)
            
            # Resolve doctor profile ID using service layer
            doctor_id = self.doctor_queue_service.get_doctor_profile_id(current_user.public_id)
            
            logger.info(
                "Completing visit",
                extra={
                    "medical_record_id": medical_record_id,
                    "user_id": str(current_user.public_id),
                    "doctor_profile_id": str(doctor_id)
                }
            )
            
            medical_record, access = self.doctor_queue_service.complete_visit(
                medical_record_id=record_id,
                doctor_id=doctor_id,
                follow_up_required=complete_data.follow_up_required,
                follow_up_date=complete_data.follow_up_date,
                follow_up_notes=complete_data.follow_up_notes
            )
            
            return CompleteVisitResponse(
                success=True,
                message="Visit marked as complete",
                medical_record_id=str(medical_record.id),
                visit_completed_at=access.visit_completed_at if access else medical_record.updated_at
            )
        
        except ValueError as e:
            logger.warning(
                "Visit completion access error",
                extra={"medical_record_id": medical_record_id, "error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to complete visit",
                extra={"medical_record_id": medical_record_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to complete visit"
            )

