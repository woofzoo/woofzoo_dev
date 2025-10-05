"""
Simple unit tests for Medical Records system (without authentication).

These tests verify the core functionality of the medical records system
by testing repositories and services directly, without HTTP layer.
"""

import pytest
from datetime import datetime, timedelta, date
import uuid


class TestMedicalRecordsRepository:
    """Test medical records repository operations."""
    
    def test_create_medical_record(self, db_session, pet, doctor_profile, clinic_profile, doctor_user):
        """Test creating a medical record."""
        from app.repositories.medical_record import MedicalRecordRepository
        from app.models.medical_record import MedicalRecord, VisitType
        
        repo = MedicalRecordRepository(db_session)
        
        record_data = MedicalRecord(
            id=uuid.uuid4(),
            pet_id=pet.id,
            visit_date=datetime.utcnow(),
            clinic_id=clinic_profile.id,
            doctor_id=doctor_profile.id,
            visit_type=VisitType.ROUTINE_CHECKUP,
            chief_complaint="Annual checkup",
            diagnosis="Healthy",
            symptoms={},
            treatment_plan="Continue regular care",
            vital_signs={},
            follow_up_required=False,
            is_emergency=False,
            created_by_user_id=doctor_user.public_id,
            created_by_role="doctor"
        )
        
        result = repo.create(record_data)
        assert result.id is not None
        assert result.pet_id == pet.id
        assert result.visit_type == VisitType.ROUTINE_CHECKUP
    
    def test_get_medical_records_by_pet(self, db_session, medical_record):
        """Test retrieving medical records for a pet."""
        from app.repositories.medical_record import MedicalRecordRepository
        
        repo = MedicalRecordRepository(db_session)
        records = repo.get_by_pet_id(medical_record.pet_id)
        
        assert len(records) > 0
        assert records[0].pet_id == medical_record.pet_id
    
    def test_get_emergency_records(self, db_session, pet, doctor_profile, clinic_profile, doctor_user):
        """Test filtering emergency records."""
        from app.repositories.medical_record import MedicalRecordRepository
        from app.models.medical_record import MedicalRecord, VisitType
        
        repo = MedicalRecordRepository(db_session)
        
        # Create emergency record
        emergency_record = MedicalRecord(
            id=uuid.uuid4(),
            pet_id=pet.id,
            visit_date=datetime.utcnow(),
            clinic_id=clinic_profile.id,
            doctor_id=doctor_profile.id,
            visit_type=VisitType.EMERGENCY,
            diagnosis="Emergency condition",
            symptoms={},
            vital_signs={},
            follow_up_required=True,
            is_emergency=True,
            created_by_user_id=doctor_user.public_id,
            created_by_role="doctor"
        )
        repo.create(emergency_record)
        
        # Get emergency records
        emergency_records = repo.get_emergency_records(pet.id)
        assert len(emergency_records) > 0
        assert all(r.is_emergency for r in emergency_records)


class TestPrescriptionRepository:
    """Test prescription repository operations."""
    
    def test_create_prescription(self, db_session, medical_record, pet, doctor_profile):
        """Test creating a prescription."""
        from app.repositories.prescription import PrescriptionRepository
        from app.models.prescription import Prescription
        
        repo = PrescriptionRepository(db_session)
        
        prescription = Prescription(
            id=uuid.uuid4(),
            medical_record_id=medical_record.id,
            pet_id=pet.id,
            medication_name="Amoxicillin",
            dosage="250",
            dosage_unit="mg",
            frequency="Twice daily",
            route="Oral",
            duration="10 days",
            prescribed_by_doctor_id=doctor_profile.id,
            prescribed_date=date.today(),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            quantity=20.0,
            refills_allowed=0,
            is_active=True
        )
        
        result = repo.create(prescription)
        assert result.id is not None
        assert result.medication_name == "Amoxicillin"
        assert result.dosage == "250"
    
    def test_get_active_prescriptions(self, db_session, prescription):
        """Test retrieving active prescriptions."""
        from app.repositories.prescription import PrescriptionRepository
        
        repo = PrescriptionRepository(db_session)
        prescriptions = repo.get_active_by_pet_id(prescription.pet_id)
        
        assert len(prescriptions) > 0
        assert all(p.is_active for p in prescriptions)


class TestAllergyRepository:
    """Test allergy repository operations."""
    
    def test_create_allergy(self, db_session, pet, owner_user):
        """Test creating an allergy record."""
        from app.repositories.allergy import AllergyRepository
        from app.models.allergy import Allergy, AllergyType, AllergySeverity
        
        repo = AllergyRepository(db_session)
        
        allergy = Allergy(
            id=uuid.uuid4(),
            pet_id=pet.id,
            allergen="Chicken",
            allergy_type=AllergyType.FOOD,
            severity=AllergySeverity.MODERATE,
            symptoms={"itching": True},
            is_active=True,
            created_by_user_id=owner_user.public_id
        )
        
        result = repo.create(allergy)
        assert result.id is not None
        assert result.allergen == "Chicken"
        assert result.allergy_type == AllergyType.FOOD
    
    def test_get_critical_allergies(self, db_session, pet, owner_user):
        """Test retrieving critical allergies."""
        from app.repositories.allergy import AllergyRepository
        from app.models.allergy import Allergy, AllergyType, AllergySeverity
        
        repo = AllergyRepository(db_session)
        
        # Create severe allergy
        allergy = Allergy(
            id=uuid.uuid4(),
            pet_id=pet.id,
            allergen="Penicillin",
            allergy_type=AllergyType.MEDICATION,
            severity=AllergySeverity.SEVERE,
            symptoms={},
            is_active=True,
            created_by_user_id=owner_user.public_id
        )
        repo.create(allergy)
        
        # Get critical allergies
        critical = repo.get_critical_by_pet_id(pet.id)
        assert len(critical) > 0
        assert all(a.severity in [AllergySeverity.SEVERE, AllergySeverity.LIFE_THREATENING] for a in critical)


class TestClinicAccessRepository:
    """Test clinic access repository operations."""
    
    def test_create_clinic_access(self, db_session, pet, clinic_profile, doctor_profile, owner_user):
        """Test creating clinic access record."""
        from app.repositories.pet_clinic_access import PetClinicAccessRepository
        from app.models.pet_clinic_access import PetClinicAccess, AccessStatus
        
        repo = PetClinicAccessRepository(db_session)
        
        access = PetClinicAccess(
            id=uuid.uuid4(),
            pet_id=pet.id,
            clinic_id=clinic_profile.id,
            doctor_id=doctor_profile.id,
            owner_id=owner_user.public_id,
            access_granted_at=datetime.utcnow(),
            access_expires_at=datetime.utcnow() + timedelta(hours=24),
            status=AccessStatus.ACTIVE,
            purpose="Annual checkup"
        )
        
        result = repo.create(access)
        assert result.id is not None
        assert result.status == AccessStatus.ACTIVE
    
    def test_get_active_access(self, db_session, active_clinic_access):
        """Test retrieving active clinic access."""
        from app.repositories.pet_clinic_access import PetClinicAccessRepository
        
        repo = PetClinicAccessRepository(db_session)
        access = repo.get_active_access(
            active_clinic_access.pet_id,
            active_clinic_access.clinic_id
        )
        
        assert access is not None
        assert access.status == "active"


class TestVaccinationRepository:
    """Test vaccination repository operations."""
    
    def test_create_vaccination(self, db_session, pet, doctor_profile, clinic_profile):
        """Test creating a vaccination record."""
        from app.repositories.vaccination import VaccinationRepository
        from app.models.vaccination import Vaccination
        
        repo = VaccinationRepository(db_session)
        
        vaccination = Vaccination(
            id=uuid.uuid4(),
            pet_id=pet.id,
            vaccine_name="Rabies",
            vaccine_type="Core",
            administered_by_doctor_id=doctor_profile.id,
            administered_at=datetime.utcnow(),
            clinic_id=clinic_profile.id,
            next_due_date=date.today() + timedelta(days=365),
            is_booster=False,
            is_required_by_law=True
        )
        
        result = repo.create(vaccination)
        assert result.id is not None
        assert result.vaccine_name == "Rabies"
        assert result.is_required_by_law is True
    
    def test_get_due_vaccinations(self, db_session, pet, doctor_profile, clinic_profile):
        """Test retrieving due vaccinations."""
        from app.repositories.vaccination import VaccinationRepository
        from app.models.vaccination import Vaccination
        
        repo = VaccinationRepository(db_session)
        
        # Create vaccination due soon
        vaccination = Vaccination(
            id=uuid.uuid4(),
            pet_id=pet.id,
            vaccine_name="DHPP",
            vaccine_type="Core",
            administered_by_doctor_id=doctor_profile.id,
            administered_at=datetime.utcnow() - timedelta(days=300),
            clinic_id=clinic_profile.id,
            next_due_date=date.today() + timedelta(days=7),
            is_booster=True,
            is_required_by_law=False
        )
        repo.create(vaccination)
        
        # Get due vaccinations
        due = repo.get_due_vaccinations(pet.id)
        assert len(due) > 0


class TestLabTestRepository:
    """Test lab test repository operations."""
    
    def test_create_lab_test(self, db_session, pet, doctor_profile):
        """Test creating a lab test."""
        from app.repositories.lab_test import LabTestRepository
        from app.models.lab_test import LabTest, TestStatus
        
        repo = LabTestRepository(db_session)
        
        lab_test = LabTest(
            id=uuid.uuid4(),
            pet_id=pet.id,
            test_name="Complete Blood Count",
            test_type="Blood Work",
            ordered_by_doctor_id=doctor_profile.id,
            ordered_at=datetime.utcnow(),
            status=TestStatus.ORDERED,
            results_json={},
            reference_ranges={},
            abnormal_flags={},
            is_abnormal=False
        )
        
        result = repo.create(lab_test)
        assert result.id is not None
        assert result.test_name == "Complete Blood Count"
        assert result.status == TestStatus.ORDERED


# Summary test
def test_medical_records_system_integration(db_session, pet, doctor_profile, clinic_profile, doctor_user, owner_user):
    """Integration test for complete medical records workflow."""
    from app.repositories.medical_record import MedicalRecordRepository
    from app.repositories.prescription import PrescriptionRepository
    from app.repositories.allergy import AllergyRepository
    from app.models.medical_record import MedicalRecord, VisitType
    from app.models.prescription import Prescription
    from app.models.allergy import Allergy, AllergyType, AllergySeverity
    
    # 1. Create medical record
    medical_repo = MedicalRecordRepository(db_session)
    record = MedicalRecord(
        id=uuid.uuid4(),
        pet_id=pet.id,
        visit_date=datetime.utcnow(),
        clinic_id=clinic_profile.id,
        doctor_id=doctor_profile.id,
        visit_type=VisitType.ROUTINE_CHECKUP,
        diagnosis="Healthy, prescribed antibiotics",
        symptoms={},
        vital_signs={"temperature": 38.5, "weight": 25.0},
        follow_up_required=False,
        is_emergency=False,
        created_by_user_id=doctor_user.public_id,
        created_by_role="doctor"
    )
    medical_record = medical_repo.create(record)
    assert medical_record.id is not None
    
    # 2. Add prescription
    prescription_repo = PrescriptionRepository(db_session)
    prescription = Prescription(
        id=uuid.uuid4(),
        medical_record_id=medical_record.id,
        pet_id=pet.id,
        medication_name="Amoxicillin",
        dosage="250",
        dosage_unit="mg",
        frequency="Twice daily",
        route="Oral",
        duration="7 days",
        prescribed_by_doctor_id=doctor_profile.id,
        prescribed_date=date.today(),
        start_date=date.today(),
        quantity=14.0,
        refills_allowed=0,
        is_active=True
    )
    rx = prescription_repo.create(prescription)
    assert rx.id is not None
    
    # 3. Add allergy (owner adds this at home)
    allergy_repo = AllergyRepository(db_session)
    allergy = Allergy(
        id=uuid.uuid4(),
        pet_id=pet.id,
        allergen="Chicken",
        allergy_type=AllergyType.FOOD,
        severity=AllergySeverity.MILD,
        symptoms={"itching": True},
        is_active=True,
        created_by_user_id=owner_user.public_id
    )
    allergy_record = allergy_repo.create(allergy)
    assert allergy_record.id is not None
    
    # 4. Verify complete medical history
    records = medical_repo.get_by_pet_id(pet.id)
    assert len(records) >= 1
    
    prescriptions = prescription_repo.get_by_pet_id(pet.id)
    assert len(prescriptions) >= 1
    
    allergies = allergy_repo.get_by_pet_id(pet.id)
    assert len(allergies) >= 1
    
    print(f"✅ Complete medical workflow test passed:")
    print(f"   - Medical records: {len(records)}")
    print(f"   - Prescriptions: {len(prescriptions)}")
    print(f"   - Allergies: {len(allergies)}")

