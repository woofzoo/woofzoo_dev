# Doctor Medical Records API Guide

**Date**: October 20, 2025  
**Audience**: Doctors  
**Purpose**: Complete guide for adding medical records, medications, prescriptions, allergies, lab tests, and vaccinations

---

## 📋 Table of Contents

1. [Doctor Workflow Overview](#doctor-workflow-overview)
2. [Visit Management APIs](#visit-management-apis)
3. [Prescription APIs](#prescription-apis)
4. [Allergy APIs](#allergy-apis)
5. [Vaccination APIs](#vaccination-apis)
6. [Lab Test APIs](#lab-test-apis)
7. [Medical Record APIs](#medical-record-apis)
8. [Complete Example Workflow](#complete-example-workflow)

---

## Doctor Workflow Overview

### Typical Doctor Visit Flow

```
1. View Today's Queue
   ↓
2. Select Pet/Visit
   ↓
3. Get Visit Details (includes medical history, allergies, vaccinations)
   ↓
4. During Consultation:
   - Update visit details (diagnosis, treatment plan, notes)
   - Add prescriptions/medications
   - Add/update allergies
   - Order lab tests
   - Add vaccinations
   ↓
5. Complete Visit
```

---

## Visit Management APIs

### 1. Get Today's Queue

**Endpoint**: `GET /api/doctor/queue/today`  
**Authorization**: Requires `doctor` role  
**Description**: View all pets assigned to you today

**Response**:
```json
{
  "date": "2025-10-20",
  "queue": [
    {
      "queue_position": 1,
      "pet": {
        "id": "uuid",
        "pet_id": "DOG-GOLDEN-000001",
        "name": "Buddy",
        "pet_type": "DOG",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_name": "John Doe"
      },
      "visit_info": {
        "medical_record_id": "uuid",
        "visit_type": "GENERAL",
        "chief_complaint": "Limping on right front leg",
        "assigned_at": "2025-10-20T09:30:00Z",
        "pre_checks": {
          "weight": 25.5,
          "temperature": 38.5,
          "heart_rate": 110,
          "respiratory_rate": 22,
          "notes": "Pet seems anxious"
        }
      },
      "status": "WITH_DOCTOR"
    }
  ],
  "total_today": 5,
  "completed": 2,
  "in_progress": 3
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/doctor/queue/today" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 2. Get Visit Details

**Endpoint**: `GET /api/doctor/visits/{medical_record_id}`  
**Authorization**: Requires `doctor` role  
**Description**: Get complete pet details, current visit, and medical history

**Response**:
```json
{
  "pet": {
    "id": "uuid",
    "pet_id": "DOG-GOLDEN-000001",
    "name": "Buddy",
    "pet_type": "DOG",
    "breed": "Golden Retriever",
    "age": 3,
    "gender": "MALE",
    "weight": 25.5,
    "owner": {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890"
    }
  },
  "current_visit": {
    "id": "uuid",
    "visit_date": "2025-10-20T09:30:00Z",
    "visit_type": "GENERAL",
    "chief_complaint": "Limping on right front leg",
    "diagnosis": null,
    "treatment_plan": null,
    "clinical_notes": null,
    "vital_signs": {
      "weight": 25.5,
      "temperature": 38.5,
      "heart_rate": 110,
      "respiratory_rate": 22
    }
  },
  "medical_history": [
    {
      "id": "uuid",
      "visit_date": "2025-09-15",
      "visit_type": "VACCINATION",
      "diagnosis": "Annual checkup",
      "treatment_plan": "Rabies vaccination administered",
      "doctor_name": "Dr. Smith",
      "clinic_name": "Happy Paws Clinic"
    }
  ],
  "allergies": [],
  "vaccinations": []
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/doctor/visits/{medical_record_id}" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Update Visit Details

**Endpoint**: `PATCH /api/doctor/visits/{medical_record_id}`  
**Authorization**: Requires `doctor` role  
**Description**: Update diagnosis, treatment plan, clinical notes, and vital signs

**Request Body**:
```json
{
  "diagnosis": "Sprained right front leg due to excessive play",
  "treatment_plan": "Rest for 2 weeks, anti-inflammatory medication, follow-up in 10 days",
  "clinical_notes": "Pet shows moderate pain on palpation. X-ray shows no fractures. Ligament strain suspected.",
  "weight": 25.8,
  "temperature": 38.3,
  "vital_signs": {
    "heart_rate": 105,
    "respiratory_rate": 20,
    "blood_pressure": "120/80",
    "mucous_membrane_color": "pink",
    "capillary_refill_time": "< 2 seconds"
  }
}
```

**Response**:
```json
{
  "success": true,
  "message": "Visit details updated successfully",
  "medical_record_id": "uuid"
}
```

**cURL Example**:
```bash
curl -X PATCH "http://localhost:8000/api/doctor/visits/{medical_record_id}" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "diagnosis": "Sprained right front leg",
    "treatment_plan": "Rest and medication",
    "clinical_notes": "Moderate pain on palpation"
  }'
```

---

### 4. Complete Visit

**Endpoint**: `POST /api/doctor/visits/{medical_record_id}/complete`  
**Authorization**: Requires `doctor` role  
**Description**: Mark visit as complete and remove from queue

**Request Body**:
```json
{
  "follow_up_required": true,
  "follow_up_date": "2025-10-30",
  "follow_up_notes": "Check leg mobility and pain levels. May need physical therapy if no improvement."
}
```

**Response**:
```json
{
  "success": true,
  "message": "Visit marked as complete",
  "medical_record_id": "uuid",
  "visit_completed_at": "2025-10-20T10:45:00Z"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/doctor/visits/{medical_record_id}/complete" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "follow_up_required": true,
    "follow_up_date": "2025-10-30",
    "follow_up_notes": "Check leg mobility"
  }'
```

---

## Prescription APIs

### 1. Add Prescription (Medication)

**Endpoint**: `POST /api/prescriptions/`  
**Authorization**: Any authenticated user (permissions checked internally)  
**Description**: Create a new prescription/medication record

**Request Body**:
```json
{
  "pet_id": "uuid",
  "medical_record_id": "uuid",
  "medication_name": "Carprofen",
  "dosage": "50mg",
  "frequency": "Twice daily (morning and evening)",
  "duration_days": 14,
  "instructions": "Give with food. Do not exceed recommended dosage.",
  "prescribed_date": "2025-10-20",
  "refills_allowed": 1,
  "notes": "Monitor for signs of stomach upset. Contact if vomiting occurs."
}
```

**Response**:
```json
{
  "id": "uuid",
  "pet_id": "uuid",
  "medical_record_id": "uuid",
  "medication_name": "Carprofen",
  "dosage": "50mg",
  "frequency": "Twice daily",
  "duration_days": 14,
  "instructions": "Give with food",
  "prescribed_date": "2025-10-20",
  "refills_allowed": 1,
  "refills_used": 0,
  "notes": "Monitor for stomach upset",
  "is_active": true,
  "created_at": "2025-10-20T10:30:00Z"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/prescriptions/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "uuid",
    "medical_record_id": "uuid",
    "medication_name": "Carprofen",
    "dosage": "50mg",
    "frequency": "Twice daily",
    "duration_days": 14,
    "instructions": "Give with food"
  }'
```

---

### 2. Get Prescriptions for Pet

**Endpoint**: `GET /api/prescriptions/pet/{pet_id}`  
**Query Parameters**: 
- `skip` (default: 0)
- `limit` (default: 100, max: 1000)

**Response**: List of prescriptions for the pet

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/prescriptions/pet/{pet_id}?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Update Prescription

**Endpoint**: `PUT /api/prescriptions/{prescription_id}`  
**Description**: Update prescription details (e.g., extend duration, add notes)

**Request Body**:
```json
{
  "dosage": "75mg",
  "duration_days": 21,
  "notes": "Increased dosage due to continued pain"
}
```

**cURL Example**:
```bash
curl -X PUT "http://localhost:8000/api/prescriptions/{prescription_id}" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "duration_days": 21,
    "notes": "Extended treatment period"
  }'
```

---

## Allergy APIs

### 1. Add Allergy

**Endpoint**: `POST /api/allergies/`  
**Authorization**: Any authenticated user (permissions checked internally)  
**Description**: Record a new allergy for a pet

**Request Body**:
```json
{
  "pet_id": "uuid",
  "allergen": "Penicillin",
  "reaction": "Severe skin rash and difficulty breathing",
  "severity": "SEVERE",
  "diagnosed_date": "2025-10-20",
  "notes": "Anaphylactic reaction observed. NEVER administer penicillin or derivatives."
}
```

**Severity Levels**: `MILD`, `MODERATE`, `SEVERE`, `LIFE_THREATENING`

**Response**:
```json
{
  "id": "uuid",
  "pet_id": "uuid",
  "allergen": "Penicillin",
  "reaction": "Severe skin rash and difficulty breathing",
  "severity": "SEVERE",
  "diagnosed_date": "2025-10-20",
  "notes": "Anaphylactic reaction observed",
  "is_active": true,
  "created_at": "2025-10-20T10:30:00Z"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/allergies/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "uuid",
    "allergen": "Penicillin",
    "reaction": "Severe rash",
    "severity": "SEVERE",
    "diagnosed_date": "2025-10-20"
  }'
```

---

### 2. Get All Allergies for Pet

**Endpoint**: `GET /api/allergies/pet/{pet_id}`  
**Description**: Get all known allergies for a pet

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/allergies/pet/{pet_id}" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Get Critical Allergies

**Endpoint**: `GET /api/allergies/pet/{pet_id}/critical`  
**Description**: Get only severe and life-threatening allergies (important before prescribing)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/allergies/pet/{pet_id}/critical" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Vaccination APIs

### 1. Add Vaccination

**Endpoint**: `POST /api/vaccinations/`  
**Authorization**: Any authenticated user (permissions checked internally)  
**Description**: Record a vaccination administered to a pet

**Request Body**:
```json
{
  "pet_id": "uuid",
  "vaccine_name": "Rabies",
  "manufacturer": "Zoetis",
  "batch_number": "RB-2025-1234",
  "administered_date": "2025-10-20",
  "next_due_date": "2026-10-20",
  "administered_by": "Dr. Jane Smith",
  "clinic_name": "Happy Paws Veterinary Clinic",
  "site": "Right shoulder",
  "route": "Subcutaneous",
  "dose": "1ml",
  "notes": "No adverse reactions observed. Pet tolerated injection well."
}
```

**Response**:
```json
{
  "id": "uuid",
  "pet_id": "uuid",
  "vaccine_name": "Rabies",
  "manufacturer": "Zoetis",
  "batch_number": "RB-2025-1234",
  "administered_date": "2025-10-20",
  "next_due_date": "2026-10-20",
  "administered_by": "Dr. Jane Smith",
  "clinic_name": "Happy Paws Veterinary Clinic",
  "site": "Right shoulder",
  "route": "Subcutaneous",
  "dose": "1ml",
  "notes": "No adverse reactions",
  "created_at": "2025-10-20T10:30:00Z"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/vaccinations/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "uuid",
    "vaccine_name": "Rabies",
    "manufacturer": "Zoetis",
    "batch_number": "RB-2025-1234",
    "administered_date": "2025-10-20",
    "next_due_date": "2026-10-20",
    "administered_by": "Dr. Jane Smith"
  }'
```

---

### 2. Get All Vaccinations for Pet

**Endpoint**: `GET /api/vaccinations/pet/{pet_id}`  
**Description**: Get complete vaccination history

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/vaccinations/pet/{pet_id}" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Get Due Vaccinations

**Endpoint**: `GET /api/vaccinations/pet/{pet_id}/due`  
**Description**: Get vaccinations that are due or overdue (useful for preventive care)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/vaccinations/pet/{pet_id}/due" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Lab Test APIs

### 1. Order Lab Test

**Endpoint**: `POST /api/lab-tests/`  
**Authorization**: Any authenticated user (permissions checked internally)  
**Description**: Order a new lab test for a pet

**Request Body**:
```json
{
  "pet_id": "uuid",
  "medical_record_id": "uuid",
  "test_type": "Blood Chemistry Panel",
  "test_name": "Complete Blood Count (CBC) + Chemistry",
  "ordered_date": "2025-10-20",
  "lab_name": "VetLab Diagnostics",
  "reason": "Check liver and kidney function due to medication",
  "priority": "ROUTINE",
  "notes": "Fasting sample required"
}
```

**Priority Levels**: `ROUTINE`, `URGENT`, `STAT`

**Response**:
```json
{
  "id": "uuid",
  "pet_id": "uuid",
  "medical_record_id": "uuid",
  "test_type": "Blood Chemistry Panel",
  "test_name": "Complete Blood Count + Chemistry",
  "status": "ORDERED",
  "ordered_date": "2025-10-20",
  "sample_collected_date": null,
  "results_date": null,
  "lab_name": "VetLab Diagnostics",
  "reason": "Check liver and kidney function",
  "priority": "ROUTINE",
  "results": null,
  "abnormal_findings": null,
  "notes": "Fasting sample required",
  "created_at": "2025-10-20T10:30:00Z"
}
```

**Status Values**: `ORDERED`, `SAMPLE_COLLECTED`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/lab-tests/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "uuid",
    "medical_record_id": "uuid",
    "test_type": "Blood Chemistry Panel",
    "test_name": "CBC + Chemistry",
    "ordered_date": "2025-10-20",
    "reason": "Check organ function"
  }'
```

---

### 2. Update Lab Test (Add Results)

**Endpoint**: `PUT /api/lab-tests/{lab_test_id}`  
**Description**: Update lab test with results when available

**Request Body**:
```json
{
  "status": "COMPLETED",
  "sample_collected_date": "2025-10-20",
  "results_date": "2025-10-22",
  "results": {
    "WBC": "7.2 K/uL (normal: 6-17)",
    "RBC": "6.8 M/uL (normal: 5.5-8.5)",
    "Hemoglobin": "15.2 g/dL (normal: 12-18)",
    "ALT": "42 U/L (normal: 10-100)",
    "Creatinine": "1.1 mg/dL (normal: 0.5-1.5)"
  },
  "abnormal_findings": null,
  "notes": "All values within normal range. Liver and kidney function normal."
}
```

**cURL Example**:
```bash
curl -X PUT "http://localhost:8000/api/lab-tests/{lab_test_id}" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "COMPLETED",
    "results_date": "2025-10-22",
    "results": {"WBC": "7.2 K/uL"},
    "notes": "All values normal"
  }'
```

---

### 3. Get Lab Tests for Pet

**Endpoint**: `GET /api/lab-tests/pet/{pet_id}`  
**Description**: Get all lab tests for a pet

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/lab-tests/pet/{pet_id}" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 4. Get Abnormal Lab Results

**Endpoint**: `GET /api/lab-tests/pet/{pet_id}/abnormal`  
**Description**: Get only tests with abnormal findings (useful for quick review)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/lab-tests/pet/{pet_id}/abnormal" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Medical Record APIs

### 1. Create Medical Record

**Endpoint**: `POST /api/medical-records/`  
**Description**: Create a standalone medical record (usually done by clinic during assignment)

**Request Body**:
```json
{
  "pet_id": "uuid",
  "doctor_id": "uuid",
  "clinic_id": "uuid",
  "visit_date": "2025-10-20",
  "visit_type": "GENERAL",
  "chief_complaint": "Limping",
  "vital_signs": {
    "weight": 25.5,
    "temperature": 38.5
  }
}
```

**Visit Types**: `GENERAL`, `EMERGENCY`, `FOLLOW_UP`, `VACCINATION`, `SURGERY`, `DENTAL`

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/medical-records/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "uuid",
    "doctor_id": "uuid",
    "clinic_id": "uuid",
    "visit_date": "2025-10-20",
    "visit_type": "GENERAL"
  }'
```

---

### 2. Get Medical Records for Pet

**Endpoint**: `GET /api/medical-records/pet/{pet_id}`  
**Query Parameters**:
- `skip` (default: 0)
- `limit` (default: 100, max: 1000)

**Description**: Get complete medical history

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/medical-records/pet/{pet_id}?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Get Medical Records by Date Range

**Endpoint**: `GET /api/medical-records/pet/{pet_id}/date-range`  
**Query Parameters**:
- `start_date` (ISO format: 2025-01-01)
- `end_date` (ISO format: 2025-12-31)
- `skip`, `limit`

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/medical-records/pet/{pet_id}/date-range?start_date=2025-01-01&end_date=2025-12-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 4. Get Emergency Records

**Endpoint**: `GET /api/medical-records/pet/{pet_id}/emergency`  
**Description**: Get only emergency visit records

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/medical-records/pet/{pet_id}/emergency" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Complete Example Workflow

### Scenario: Dog with Leg Injury

Here's a complete workflow for a doctor treating a dog with a leg injury:

```bash
# Step 1: Get today's queue
curl -X GET "http://localhost:8000/api/doctor/queue/today" \
  -H "Authorization: Bearer $TOKEN"

# Response shows medical_record_id: "mr-123"

# Step 2: Get visit details
curl -X GET "http://localhost:8000/api/doctor/visits/mr-123" \
  -H "Authorization: Bearer $TOKEN"

# Step 3: Check for critical allergies before prescribing
curl -X GET "http://localhost:8000/api/allergies/pet/pet-456/critical" \
  -H "Authorization: Bearer $TOKEN"

# Step 4: Update visit with diagnosis and treatment plan
curl -X PATCH "http://localhost:8000/api/doctor/visits/mr-123" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "diagnosis": "Sprained right front leg",
    "treatment_plan": "Rest for 2 weeks, anti-inflammatory medication",
    "clinical_notes": "Moderate pain on palpation. No fractures on X-ray.",
    "weight": 25.8,
    "temperature": 38.3
  }'

# Step 5: Prescribe anti-inflammatory medication
curl -X POST "http://localhost:8000/api/prescriptions/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "pet-456",
    "medical_record_id": "mr-123",
    "medication_name": "Carprofen",
    "dosage": "50mg",
    "frequency": "Twice daily",
    "duration_days": 14,
    "instructions": "Give with food"
  }'

# Step 6: Order lab test to monitor kidney function (NSAID safety)
curl -X POST "http://localhost:8000/api/lab-tests/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "pet-456",
    "medical_record_id": "mr-123",
    "test_type": "Blood Chemistry",
    "test_name": "Kidney Function Panel",
    "ordered_date": "2025-10-20",
    "reason": "Monitor kidney function while on NSAIDs",
    "priority": "ROUTINE"
  }'

# Step 7: Complete visit with follow-up
curl -X POST "http://localhost:8000/api/doctor/visits/mr-123/complete" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "follow_up_required": true,
    "follow_up_date": "2025-10-30",
    "follow_up_notes": "Check leg mobility and pain levels. Review lab results."
  }'
```

---

## API Summary Table

| Feature | Endpoint | Method | Description |
|---------|----------|--------|-------------|
| **Visit Management** |
| Today's Queue | `/api/doctor/queue/today` | GET | View assigned pets |
| Visit Details | `/api/doctor/visits/{id}` | GET | Get pet + history |
| Update Visit | `/api/doctor/visits/{id}` | PATCH | Add diagnosis/treatment |
| Complete Visit | `/api/doctor/visits/{id}/complete` | POST | Mark as done |
| **Prescriptions** |
| Add Medication | `/api/prescriptions/` | POST | Prescribe medication |
| Get by Pet | `/api/prescriptions/pet/{pet_id}` | GET | View prescriptions |
| Update Prescription | `/api/prescriptions/{id}` | PUT | Modify prescription |
| **Allergies** |
| Add Allergy | `/api/allergies/` | POST | Record allergy |
| Get by Pet | `/api/allergies/pet/{pet_id}` | GET | View all allergies |
| Critical Only | `/api/allergies/pet/{pet_id}/critical` | GET | View severe allergies |
| **Vaccinations** |
| Add Vaccination | `/api/vaccinations/` | POST | Record vaccination |
| Get by Pet | `/api/vaccinations/pet/{pet_id}` | GET | View vaccination history |
| Due Vaccines | `/api/vaccinations/pet/{pet_id}/due` | GET | View due vaccinations |
| **Lab Tests** |
| Order Test | `/api/lab-tests/` | POST | Order lab test |
| Add Results | `/api/lab-tests/{id}` | PUT | Update with results |
| Get by Pet | `/api/lab-tests/pet/{pet_id}` | GET | View all tests |
| Abnormal Results | `/api/lab-tests/pet/{pet_id}/abnormal` | GET | View abnormal only |
| **Medical Records** |
| Create Record | `/api/medical-records/` | POST | Create new record |
| Get by Pet | `/api/medical-records/pet/{pet_id}` | GET | View history |
| Date Range | `/api/medical-records/pet/{pet_id}/date-range` | GET | Filter by dates |
| Emergency Only | `/api/medical-records/pet/{pet_id}/emergency` | GET | View emergencies |

---

## Authentication

All endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

Get your token by logging in:

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@example.com",
    "password": "your_password"
  }'
```

---

## Permissions

- **Doctor Role Required**: Visit management endpoints (`/api/doctor/*`)
- **Permission Checked**: Other endpoints check if you have permission to access the pet's data
  - Pet owner (admin)
  - Family member with appropriate permissions
  - Clinic/doctor with active access

---

## Best Practices

### 1. Always Check Allergies First
```bash
# Before prescribing, always check critical allergies
GET /api/allergies/pet/{pet_id}/critical
```

### 2. Complete Visit Last
Complete the visit only after:
- ✅ Diagnosis updated
- ✅ Treatment plan documented
- ✅ Prescriptions added
- ✅ Lab tests ordered (if needed)
- ✅ Vaccinations recorded (if given)

### 3. Use Follow-up for Continuity
Always specify follow-up requirements when completing visits:
```json
{
  "follow_up_required": true,
  "follow_up_date": "2025-11-01",
  "follow_up_notes": "Check wound healing, remove sutures"
}
```

### 4. Document Thoroughly
Include detailed clinical notes:
```json
{
  "clinical_notes": "Physical exam findings: ..., Diagnostic reasoning: ..., Treatment rationale: ..."
}
```

---

## Error Handling

Common error responses:

**403 Forbidden**:
```json
{
  "detail": "You do not have permission to access this pet's records"
}
```

**404 Not Found**:
```json
{
  "detail": "Medical record not found"
}
```

**400 Bad Request**:
```json
{
  "detail": "Invalid data provided",
  "errors": {
    "dosage": "Field required"
  }
}
```

---

## Support

For API issues or questions:
- Check logs: `logs/app.log`
- API documentation: `http://localhost:8000/docs` (Swagger UI)
- Backend team: [Contact Info]

---

**Document Version**: 1.0  
**Last Updated**: October 20, 2025  
**Base URL**: `http://localhost:8000` (update for production)

