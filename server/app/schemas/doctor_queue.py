"""
Doctor Queue schemas for request/response validation.

This module defines Pydantic models for doctor queue operations including
viewing today's queue, pet visit details, and visit completion.
"""

from typing import Optional, List
from datetime import datetime
from datetime import date as date_type
import uuid

from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Queue Schemas
# ============================================================================

class PetQueueInfo(BaseModel):
    """Basic pet information in doctor's queue."""
    
    id: str = Field(..., description="Pet UUID")
    pet_id: str = Field(..., description="Pet readable ID")
    name: str = Field(..., description="Pet name")
    pet_type: str = Field(..., description="Pet type")
    breed: str = Field(..., description="Pet breed")
    age: Optional[int] = Field(None, description="Pet age")
    owner_name: str = Field(..., description="Owner's full name")
    
    model_config = ConfigDict(from_attributes=True)


class VisitInfo(BaseModel):
    """Visit information for queue item."""
    
    medical_record_id: str = Field(..., description="Medical record UUID")
    visit_type: str = Field(..., description="Type of visit")
    chief_complaint: Optional[str] = Field(None, description="Reason for visit")
    assigned_at: datetime = Field(..., description="When assigned to doctor")
    pre_checks: Optional[dict] = Field(None, description="Pre-check vitals")
    
    model_config = ConfigDict(from_attributes=True)


class DoctorQueueItem(BaseModel):
    """Single item in doctor's queue."""
    
    queue_position: int = Field(..., description="Position in queue")
    pet: PetQueueInfo = Field(..., description="Pet information")
    visit_info: VisitInfo = Field(..., description="Visit information")
    status: str = Field(..., description="Queue status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "queue_position": 1,
                "pet": {
                    "id": "uuid",
                    "pet_id": "DOG-001",
                    "name": "Buddy",
                    "pet_type": "DOG",
                    "breed": "Golden Retriever",
                    "age": 3,
                    "owner_name": "John Doe"
                },
                "visit_info": {
                    "medical_record_id": "uuid",
                    "visit_type": "ROUTINE_CHECKUP",
                    "chief_complaint": "Annual checkup",
                    "assigned_at": "2025-10-11T10:00:00Z",
                    "pre_checks": {
                        "weight": 25.5,
                        "temperature": 38.5,
                        "heart_rate": 90
                    }
                },
                "status": "with_doctor"
            }
        }
    )


class DoctorQueueResponse(BaseModel):
    """Doctor's queue for today."""
    
    date: date_type = Field(..., description="Queue date")
    queue: List[DoctorQueueItem] = Field(..., description="List of pets in queue")
    total: int = Field(..., description="Total pets assigned today")
    completed: int = Field(..., description="Number of completed visits")
    in_progress: int = Field(..., description="Number of visits in progress")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-10-11",
                "queue": [],
                "total": 5,
                "completed": 2,
                "in_progress": 3
            }
        }
    )


# ============================================================================
# Visit Details Schemas
# ============================================================================

class MedicalHistoryItem(BaseModel):
    """Single medical history entry."""
    
    id: str = Field(..., description="Medical record ID")
    visit_date: datetime = Field(..., description="Visit date")
    visit_type: str = Field(..., description="Visit type")
    diagnosis: Optional[str] = Field(None, description="Diagnosis")
    treatment_plan: Optional[str] = Field(None, description="Treatment plan")
    doctor_name: Optional[str] = Field(None, description="Doctor name")
    clinic_name: Optional[str] = Field(None, description="Clinic name")
    
    model_config = ConfigDict(from_attributes=True)


class PetVisitDetails(BaseModel):
    """Detailed pet information for current visit."""
    
    pet: dict = Field(..., description="Full pet details")
    current_visit: dict = Field(..., description="Current medical record")
    medical_history: List[MedicalHistoryItem] = Field(..., description="Past visits")
    allergies: List[dict] = Field(..., description="Known allergies")
    vaccinations: List[dict] = Field(..., description="Vaccination history")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet": {
                    "id": "uuid",
                    "name": "Buddy",
                    "pet_type": "DOG",
                    "breed": "Golden Retriever",
                    "age": 3,
                    "weight": 25.5,
                    "owner": {
                        "name": "John Doe",
                        "email": "john@example.com"
                    }
                },
                "current_visit": {
                    "id": "uuid",
                    "visit_date": "2025-10-11T10:00:00Z",
                    "visit_type": "ROUTINE_CHECKUP",
                    "chief_complaint": "Annual checkup"
                },
                "medical_history": [],
                "allergies": [],
                "vaccinations": []
            }
        }
    )


# ============================================================================
# Visit Update Schemas
# ============================================================================

class VisitUpdateRequest(BaseModel):
    """Update visit details."""
    
    diagnosis: Optional[str] = Field(None, description="Diagnosis")
    treatment_plan: Optional[str] = Field(None, description="Treatment plan")
    clinical_notes: Optional[str] = Field(None, description="Clinical notes")
    weight: Optional[float] = Field(None, ge=0.1, le=500, description="Weight in kg")
    temperature: Optional[float] = Field(None, ge=30, le=45, description="Temperature in °C")
    vital_signs: Optional[dict] = Field(None, description="Vital signs dict")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "diagnosis": "Healthy, no issues found",
                "treatment_plan": "Continue regular diet and exercise",
                "clinical_notes": "Patient is in good health...",
                "weight": 25.5,
                "temperature": 38.5,
                "vital_signs": {
                    "heart_rate": 90,
                    "respiratory_rate": 25
                }
            }
        }
    )


class VisitUpdateResponse(BaseModel):
    """Response for visit update."""
    
    success: bool = Field(..., description="Whether update was successful")
    message: str = Field(..., description="Success message")
    medical_record_id: str = Field(..., description="Updated medical record ID")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Visit details updated successfully",
                "medical_record_id": "uuid"
            }
        }
    )


# ============================================================================
# Visit Completion Schemas
# ============================================================================

class CompleteVisitRequest(BaseModel):
    """Request to complete a visit."""
    
    follow_up_required: bool = Field(False, description="Whether follow-up is needed")
    follow_up_date: Optional[date_type] = Field(None, description="Follow-up date")
    follow_up_notes: Optional[str] = Field(None, description="Follow-up instructions")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "follow_up_required": True,
                "follow_up_date": "2025-11-11",
                "follow_up_notes": "Return for booster shot"
            }
        }
    )


class CompleteVisitResponse(BaseModel):
    """Response for visit completion."""
    
    success: bool = Field(..., description="Whether completion was successful")
    message: str = Field(..., description="Success message")
    medical_record_id: str = Field(..., description="Completed medical record ID")
    visit_completed_at: datetime = Field(..., description="Completion timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Visit marked as complete",
                "medical_record_id": "uuid",
                "visit_completed_at": "2025-10-11T11:30:00Z"
            }
        }
    )

