"""
Models package for the application.

This package contains all SQLAlchemy models for the application.
"""

from app.models.user import User, UserRole
from app.models.owner import Owner
from app.models.family import Family
from app.models.family_member import FamilyMember, AccessLevel
from app.models.pet import Pet, Gender
from app.models.otp import OTP, OTPPurpose
from app.models.family_invitation import FamilyInvitation
from app.models.photo import Photo

# Medical Records System Models
from app.models.clinic_profile import ClinicProfile
from app.models.doctor_profile import DoctorProfile
from app.models.doctor_clinic_association import DoctorClinicAssociation, EmploymentType
from app.models.pet_clinic_access import PetClinicAccess, AccessStatus
from app.models.medical_record import MedicalRecord, VisitType
from app.models.prescription import Prescription
from app.models.lab_test import LabTest, TestStatus
from app.models.allergy import Allergy, AllergyType, AllergySeverity
from app.models.vaccination import Vaccination
from app.models.medical_record_attachment import MedicalRecordAttachment, AttachmentType

__all__ = [
    # User & Owner Models
    "User",
    "UserRole", 
    "Owner",
    "Family",
    "FamilyMember",
    "AccessLevel",
    "Pet",
    "Gender",
    "OTP",
    "OTPPurpose",
    "FamilyInvitation",
    "Photo",
    # Medical Records Models
    "ClinicProfile",
    "DoctorProfile",
    "DoctorClinicAssociation",
    "EmploymentType",
    "PetClinicAccess",
    "AccessStatus",
    "MedicalRecord",
    "VisitType",
    "Prescription",
    "LabTest",
    "TestStatus",
    "Allergy",
    "AllergyType",
    "AllergySeverity",
    "Vaccination",
    "MedicalRecordAttachment",
    "AttachmentType",
]
