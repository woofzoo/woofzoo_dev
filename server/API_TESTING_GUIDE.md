# Medical Records API - Complete Testing Guide with cURL

## Prerequisites

```bash
# Set your API base URL
export API_URL="http://localhost:8000"

# Get authentication token (replace with your actual login endpoint)
export AUTH_TOKEN=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@test.com",
    "password": "YourPassword123!"
  }' | jq -r '.access_token')

# Set test UUIDs (replace with actual IDs from your database)
export PET_ID="123e4567-e89b-12d3-a456-426614174000"
export CLINIC_ID="223e4567-e89b-12d3-a456-426614174000"
export DOCTOR_ID="323e4567-e89b-12d3-a456-426614174000"
export MEDICAL_RECORD_ID="423e4567-e89b-12d3-a456-426614174000"
export PRESCRIPTION_ID="523e4567-e89b-12d3-a456-426614174000"
export LAB_TEST_ID="623e4567-e89b-12d3-a456-426614174000"
```

---

## 1. Medical Records Endpoints

### Create Medical Record

```bash
curl -X POST "$API_URL/api/v1/medical-records/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "visit_date": "2025-10-01T10:30:00",
    "clinic_id": "'"$CLINIC_ID"'",
    "doctor_id": "'"$DOCTOR_ID"'",
    "visit_type": "routine_checkup",
    "chief_complaint": "Annual wellness examination",
    "diagnosis": "Healthy - no concerns",
    "symptoms": {
      "energy_level": "normal",
      "appetite": "good"
    },
    "treatment_plan": "Continue current diet and exercise",
    "clinical_notes": "Pet appears healthy. All vital signs normal.",
    "weight": 25.5,
    "temperature": 38.5,
    "vital_signs": {
      "heart_rate": 80,
      "respiratory_rate": 20
    },
    "follow_up_required": false,
    "is_emergency": false
  }'
```

### Get Medical Record by ID

```bash
curl -X GET "$API_URL/api/v1/medical-records/$MEDICAL_RECORD_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Get All Medical Records for a Pet

```bash
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID?skip=0&limit=10" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Get Medical Records by Date Range

```bash
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID/date-range?start_date=2025-01-01T00:00:00&end_date=2025-12-31T23:59:59&skip=0&limit=10" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Get Emergency Records Only

```bash
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID/emergency?skip=0&limit=10" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Update Medical Record (Admin Correction)

```bash
curl -X PUT "$API_URL/api/v1/medical-records/$MEDICAL_RECORD_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "clinical_notes": "Updated notes: Additional observation added",
    "weight": 25.8
  }'
```

---

## 2. Prescription Endpoints

### Create Prescription

```bash
curl -X POST "$API_URL/api/v1/prescriptions/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "medical_record_id": "'"$MEDICAL_RECORD_ID"'",
    "pet_id": "'"$PET_ID"'",
    "medication_name": "Amoxicillin",
    "dosage": "250",
    "dosage_unit": "mg",
    "frequency": "Twice daily",
    "route": "Oral",
    "duration": "10 days",
    "instructions": "Give with food to reduce stomach upset",
    "prescribed_by_doctor_id": "'"$DOCTOR_ID"'",
    "prescribed_date": "2025-10-01",
    "start_date": "2025-10-01",
    "end_date": "2025-10-11",
    "quantity": 20.0,
    "refills_allowed": 0,
    "is_active": true
  }'
```

### Get Prescription by ID

```bash
curl -X GET "$API_URL/api/v1/prescriptions/$PRESCRIPTION_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Get All Prescriptions for a Pet

```bash
curl -X GET "$API_URL/api/v1/prescriptions/pet/$PET_ID?skip=0&limit=10" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Update Prescription

```bash
curl -X PUT "$API_URL/api/v1/prescriptions/$PRESCRIPTION_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false,
    "instructions": "Medication completed successfully"
  }'
```

---

## 3. Allergy Endpoints

### Create Allergy Record

```bash
curl -X POST "$API_URL/api/v1/allergies/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "allergen": "Chicken",
    "allergy_type": "food",
    "severity": "moderate",
    "symptoms": {
      "itching": true,
      "vomiting": false,
      "diarrhea": true,
      "skin_rash": true
    },
    "reaction_description": "Pet develops skin rash and digestive issues within 2-4 hours of consuming chicken",
    "notes": "Owner noticed pattern over multiple incidents"
  }'
```

### Create Medication Allergy (Doctor)

```bash
curl -X POST "$API_URL/api/v1/allergies/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "allergen": "Penicillin",
    "allergy_type": "medication",
    "severity": "severe",
    "symptoms": {
      "swelling": true,
      "difficulty_breathing": true,
      "hives": true
    },
    "reaction_description": "Severe allergic reaction requiring emergency treatment",
    "diagnosed_by_doctor_id": "'"$DOCTOR_ID"'",
    "diagnosed_date": "2025-10-01",
    "notes": "CRITICAL: Do not administer penicillin or related antibiotics"
  }'
```

### Get All Allergies for a Pet

```bash
curl -X GET "$API_URL/api/v1/allergies/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Get Critical Allergies Only

```bash
curl -X GET "$API_URL/api/v1/allergies/pet/$PET_ID/critical" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

---

## 4. Vaccination Endpoints

### Create Vaccination Record

```bash
curl -X POST "$API_URL/api/v1/vaccinations/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "medical_record_id": "'"$MEDICAL_RECORD_ID"'",
    "vaccine_name": "Rabies",
    "vaccine_type": "Core Vaccine",
    "manufacturer": "Merial",
    "batch_number": "RB12345",
    "administered_by_doctor_id": "'"$DOCTOR_ID"'",
    "administered_at": "2025-10-01T10:45:00",
    "administration_site": "Left shoulder",
    "clinic_id": "'"$CLINIC_ID"'",
    "next_due_date": "2026-10-01",
    "is_booster": false,
    "is_required_by_law": true
  }'
```

### Create Booster Vaccination

```bash
curl -X POST "$API_URL/api/v1/vaccinations/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "vaccine_name": "DHPP",
    "vaccine_type": "Core Vaccine",
    "manufacturer": "Zoetis",
    "batch_number": "DH67890",
    "administered_by_doctor_id": "'"$DOCTOR_ID"'",
    "administered_at": "2025-10-01T10:50:00",
    "administration_site": "Right shoulder",
    "clinic_id": "'"$CLINIC_ID"'",
    "next_due_date": "2026-10-01",
    "is_booster": true,
    "is_required_by_law": false,
    "reaction_notes": "No adverse reactions observed"
  }'
```

### Get All Vaccinations for a Pet

```bash
curl -X GET "$API_URL/api/v1/vaccinations/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Get Due/Upcoming Vaccinations

```bash
curl -X GET "$API_URL/api/v1/vaccinations/pet/$PET_ID/due" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

---

## 5. Lab Test Endpoints

### Order Lab Test

```bash
curl -X POST "$API_URL/api/v1/lab-tests/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "medical_record_id": "'"$MEDICAL_RECORD_ID"'",
    "pet_id": "'"$PET_ID"'",
    "test_name": "Complete Blood Count (CBC)",
    "test_type": "Blood Work",
    "ordered_by_doctor_id": "'"$DOCTOR_ID"'",
    "ordered_at": "2025-10-01T11:00:00",
    "status": "ordered",
    "results_json": {},
    "reference_ranges": {},
    "abnormal_flags": {},
    "is_abnormal": false
  }'
```

### Update Lab Test with Results

```bash
curl -X PUT "$API_URL/api/v1/lab-tests/$LAB_TEST_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "performed_at": "2025-10-01T14:30:00",
    "performed_by_clinic_id": "'"$CLINIC_ID"'",
    "results": "All values within normal range",
    "results_json": {
      "WBC": 7.5,
      "RBC": 6.8,
      "Hemoglobin": 15.2,
      "Platelets": 250
    },
    "reference_ranges": {
      "WBC": "6.0-17.0",
      "RBC": "5.5-8.5",
      "Hemoglobin": "12.0-18.0",
      "Platelets": "200-500"
    },
    "abnormal_flags": {},
    "interpretation": "Normal complete blood count. No concerns.",
    "is_abnormal": false
  }'
```

### Get All Lab Tests for a Pet

```bash
curl -X GET "$API_URL/api/v1/lab-tests/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Get Abnormal Lab Results Only

```bash
curl -X GET "$API_URL/api/v1/lab-tests/pet/$PET_ID/abnormal" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

---

## 6. Clinic Access Endpoints (OTP Workflow)

### Step 1: Request Clinic Access (Generates OTP)

```bash
curl -X POST "$API_URL/api/v1/clinic-access/request" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "clinic_id": "'"$CLINIC_ID"'",
    "purpose": "Annual checkup and vaccination"
  }'
```

**Response Example:**
```json
{
  "otp_id": "723e4567-e89b-12d3-a456-426614174000",
  "otp_code": "123456",
  "expires_in_minutes": 10,
  "message": "OTP sent to pet owner's email/phone"
}
```

### Step 2: Grant Clinic Access (Validate OTP)

```bash
# Owner validates the OTP to grant access
curl -X POST "$API_URL/api/v1/clinic-access/grant" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "clinic_id": "'"$CLINIC_ID"'",
    "otp_code": "123456",
    "doctor_id": "'"$DOCTOR_ID"'",
    "access_duration_hours": 24
  }'
```

**Response Example:**
```json
{
  "access_id": "823e4567-e89b-12d3-a456-426614174000",
  "pet_id": "123e4567-e89b-12d3-a456-426614174000",
  "clinic_id": "223e4567-e89b-12d3-a456-426614174000",
  "doctor_id": "323e4567-e89b-12d3-a456-426614174000",
  "status": "active",
  "access_granted_at": "2025-10-01T09:00:00",
  "access_expires_at": "2025-10-02T09:00:00"
}
```

### Step 3: Revoke Clinic Access

```bash
curl -X POST "$API_URL/api/v1/clinic-access/revoke" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "access_id": "823e4567-e89b-12d3-a456-426614174000"
  }'
```

---

## Complete Workflow Example

### Scenario: Pet visits clinic for checkup with vaccination

```bash
#!/bin/bash

# 1. Owner requests clinic access
echo "Step 1: Requesting clinic access..."
OTP_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/clinic-access/request" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "clinic_id": "'"$CLINIC_ID"'",
    "purpose": "Annual checkup"
  }')

OTP_CODE=$(echo $OTP_RESPONSE | jq -r '.otp_code')
echo "OTP Generated: $OTP_CODE"

# 2. Owner validates OTP to grant access
echo "Step 2: Granting clinic access..."
ACCESS_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/clinic-access/grant" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "clinic_id": "'"$CLINIC_ID"'",
    "otp_code": "'"$OTP_CODE"'",
    "doctor_id": "'"$DOCTOR_ID"'",
    "access_duration_hours": 24
  }')

echo "Access Granted!"

# 3. Doctor creates medical record
echo "Step 3: Creating medical record..."
RECORD_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/medical-records/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "visit_date": "2025-10-01T10:30:00",
    "clinic_id": "'"$CLINIC_ID"'",
    "doctor_id": "'"$DOCTOR_ID"'",
    "visit_type": "routine_checkup",
    "chief_complaint": "Annual wellness exam",
    "diagnosis": "Healthy",
    "weight": 25.5,
    "temperature": 38.5,
    "is_emergency": false
  }')

RECORD_ID=$(echo $RECORD_RESPONSE | jq -r '.id')
echo "Medical Record Created: $RECORD_ID"

# 4. Doctor administers vaccination
echo "Step 4: Recording vaccination..."
curl -s -X POST "$API_URL/api/v1/vaccinations/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "medical_record_id": "'"$RECORD_ID"'",
    "vaccine_name": "Rabies",
    "vaccine_type": "Core",
    "administered_by_doctor_id": "'"$DOCTOR_ID"'",
    "administered_at": "2025-10-01T10:45:00",
    "clinic_id": "'"$CLINIC_ID"'",
    "next_due_date": "2026-10-01",
    "is_required_by_law": true
  }'

echo "Vaccination Recorded!"

# 5. Owner views complete medical history
echo "Step 5: Retrieving medical history..."
curl -s -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN" | jq '.'

echo "Workflow Complete!"
```

---

## Testing Different User Roles

### Test as Pet Owner

```bash
# Login as pet owner
OWNER_TOKEN=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@test.com",
    "password": "OwnerPass123!"
  }' | jq -r '.access_token')

# Owner can view all records
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID" \
  -H "Authorization: Bearer $OWNER_TOKEN"

# Owner can add home medication (allergy)
curl -X POST "$API_URL/api/v1/allergies/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "allergen": "Beef",
    "allergy_type": "food",
    "severity": "mild"
  }'
```

### Test as Doctor

```bash
# Login as doctor
DOCTOR_TOKEN=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@test.com",
    "password": "DoctorPass123!"
  }' | jq -r '.access_token')

# Doctor can create professional records (if clinic access is active)
curl -X POST "$API_URL/api/v1/medical-records/" \
  -H "Authorization: Bearer $DOCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "clinic_id": "'"$CLINIC_ID"'",
    "doctor_id": "'"$DOCTOR_ID"'",
    "visit_type": "emergency",
    "diagnosis": "Minor injury",
    "is_emergency": true
  }'
```

### Test as Read-Only Family Member

```bash
# Login as family member
FAMILY_TOKEN=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "family@test.com",
    "password": "FamilyPass123!"
  }' | jq -r '.access_token')

# Can view records
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID" \
  -H "Authorization: Bearer $FAMILY_TOKEN"

# Cannot create records (should fail with 403)
curl -X POST "$API_URL/api/v1/medical-records/" \
  -H "Authorization: Bearer $FAMILY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "visit_type": "other"
  }'
```

---

## Error Testing

### Test Unauthorized Access

```bash
# Try to access without token (should get 401)
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID"
```

### Test Access to Another User's Pet

```bash
# Try to access pet you don't own (should get 403)
curl -X GET "$API_URL/api/v1/medical-records/pet/999e4567-e89b-12d3-a456-426614174999" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

### Test Invalid OTP

```bash
# Try to grant access with invalid OTP (should fail)
curl -X POST "$API_URL/api/v1/clinic-access/grant" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "'"$PET_ID"'",
    "clinic_id": "'"$CLINIC_ID"'",
    "otp_code": "000000",
    "doctor_id": "'"$DOCTOR_ID"'"
  }'
```

---

## Useful Testing Helpers

### Pretty Print JSON Responses

```bash
# Add | jq '.' to any curl command
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN" | jq '.'
```

### Save Response to File

```bash
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -o medical_records.json
```

### Check HTTP Status Only

```bash
curl -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -o /dev/null -w '%{http_code}\n' -s
```

### Verbose Output (See Headers)

```bash
curl -v -X GET "$API_URL/api/v1/medical-records/pet/$PET_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

---

## Quick Reference: All Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **Medical Records** |
| POST | `/api/v1/medical-records/` | Create medical record |
| GET | `/api/v1/medical-records/{id}` | Get record by ID |
| GET | `/api/v1/medical-records/pet/{pet_id}` | Get all records for pet |
| GET | `/api/v1/medical-records/pet/{pet_id}/date-range` | Get records by date range |
| GET | `/api/v1/medical-records/pet/{pet_id}/emergency` | Get emergency records |
| PUT | `/api/v1/medical-records/{id}` | Update record |
| **Prescriptions** |
| POST | `/api/v1/prescriptions/` | Create prescription |
| GET | `/api/v1/prescriptions/{id}` | Get prescription by ID |
| GET | `/api/v1/prescriptions/pet/{pet_id}` | Get all prescriptions |
| PUT | `/api/v1/prescriptions/{id}` | Update prescription |
| **Allergies** |
| POST | `/api/v1/allergies/` | Create allergy record |
| GET | `/api/v1/allergies/pet/{pet_id}` | Get all allergies |
| GET | `/api/v1/allergies/pet/{pet_id}/critical` | Get critical allergies |
| **Vaccinations** |
| POST | `/api/v1/vaccinations/` | Create vaccination |
| GET | `/api/v1/vaccinations/pet/{pet_id}` | Get all vaccinations |
| GET | `/api/v1/vaccinations/pet/{pet_id}/due` | Get due vaccinations |
| **Lab Tests** |
| POST | `/api/v1/lab-tests/` | Order lab test |
| GET | `/api/v1/lab-tests/pet/{pet_id}` | Get all lab tests |
| GET | `/api/v1/lab-tests/pet/{pet_id}/abnormal` | Get abnormal results |
| PUT | `/api/v1/lab-tests/{id}` | Update test results |
| **Clinic Access** |
| POST | `/api/v1/clinic-access/request` | Request access (generate OTP) |
| POST | `/api/v1/clinic-access/grant` | Grant access (validate OTP) |
| POST | `/api/v1/clinic-access/revoke` | Revoke access |

---

## Next Steps

1. **Get Real UUIDs**: Replace placeholder UUIDs with actual IDs from your database
2. **Get Auth Token**: Authenticate and get a real JWT token
3. **Test Workflow**: Run the complete workflow script
4. **Test Permissions**: Try different user roles
5. **Test Edge Cases**: Invalid data, unauthorized access, etc.

**Happy Testing!** 🎉

