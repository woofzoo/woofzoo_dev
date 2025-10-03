# Profile Management Guide - Doctor & Clinic Registration

## 🎯 Overview

This guide explains how doctors and clinic owners complete their profile setup after creating a user account.

---

## ⚠️ **Critical Understanding: Two-Step Process**

### The Problem We're Solving

When you create a user account with role `"doctor"` or `"clinic_owner"`, you get:
- ✅ Entry in `users` table (authentication works)
- ❌ **NO entry in `doctor_profiles` or `clinic_profiles`**
- ❌ **Cannot create medical records yet!**

### Why Two Tables?

```
users table          →  Authentication data (email, password, roles)
doctor_profiles      →  Professional data (license, specialization)
clinic_profiles      →  Business data (clinic name, address, license)
```

**Separation of concerns**: Auth data separate from professional/business data.

---

## 🔄 **Complete User Journey**

### For Doctors

```
Step 1: Sign Up               Step 2: Create Profile         Step 3: Join Clinic
┌──────────────────┐         ┌───────────────────┐         ┌──────────────────┐
│ POST /auth/signup│         │ POST /doctor-      │         │ Clinic owner     │
│                  │    →    │   profiles/        │    →    │ adds doctor to   │
│ Creates user     │         │                    │         │ their clinic     │
│ with "doctor"    │         │ Creates doctor_    │         │                  │
│ role             │         │ profiles entry     │         │ Now can create   │
│                  │         │                    │         │ medical records! │
└──────────────────┘         └───────────────────┘         └──────────────────┘
```

### For Clinic Owners

```
Step 1: Sign Up               Step 2: Create Profile         Step 3: Add Doctors
┌──────────────────┐         ┌───────────────────┐         ┌──────────────────┐
│ POST /auth/signup│         │ POST /clinic-      │         │ Search for       │
│                  │    →    │   profiles/        │    →    │ doctors and      │
│ Creates user     │         │                    │         │ create           │
│ with "clinic_    │         │ Creates clinic_    │         │ associations     │
│ owner" role      │         │ profiles entry     │         │                  │
│                  │         │                    │         │ Clinic ready!    │
└──────────────────┘         └───────────────────┘         └──────────────────┘
```

---

## 📝 **API Endpoints**

### 1. Doctor Profile Management

#### Create Doctor Profile (After Signup)

```bash
POST /api/v1/doctor-profiles/

# Must be called by authenticated user with "doctor" role
# Creates the doctor_profiles entry
```

**Request:**
```json
{
  "license_number": "VET-12345",
  "specialization": "General Practice",
  "years_of_experience": 5,
  "qualifications": [
    {
      "degree": "Doctor of Veterinary Medicine",
      "institution": "University of California",
      "year": 2018
    }
  ],
  "bio": "Experienced veterinarian specializing in small animals"
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-uuid-here",
  "license_number": "VET-12345",
  "specialization": "General Practice",
  "years_of_experience": 5,
  "is_verified": false,
  "is_active": true,
  "created_at": "2025-10-01T10:00:00"
}
```

#### Get My Doctor Profile

```bash
GET /api/v1/doctor-profiles/me
```

#### Update My Doctor Profile

```bash
PUT /api/v1/doctor-profiles/me

{
  "specialization": "Surgery",
  "years_of_experience": 6,
  "bio": "Updated bio"
}
```

#### Search Doctors (For Clinic Owners)

```bash
GET /api/v1/doctor-profiles?specialization=Surgery&is_verified=true
```

---

### 2. Clinic Profile Management

#### Create Clinic Profile (After Signup)

```bash
POST /api/v1/clinic-profiles/

# Must be called by authenticated user with "clinic_owner" role
# Creates the clinic_profiles entry
```

**Request:**
```json
{
  "clinic_name": "Happy Paws Veterinary Clinic",
  "license_number": "CLINIC-54321",
  "address": "123 Main Street, San Francisco, CA 94102",
  "phone": "+1-415-555-0123",
  "email": "contact@happypaws.com",
  "operating_hours": {
    "monday": "9:00 AM - 6:00 PM",
    "tuesday": "9:00 AM - 6:00 PM",
    "wednesday": "9:00 AM - 6:00 PM",
    "thursday": "9:00 AM - 6:00 PM",
    "friday": "9:00 AM - 6:00 PM",
    "saturday": "10:00 AM - 4:00 PM",
    "sunday": "Closed"
  },
  "services_offered": [
    "General Checkups",
    "Vaccinations",
    "Surgery",
    "Dental Care",
    "Emergency Services"
  ]
}
```

**Response:**
```json
{
  "id": "223e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-uuid-here",
  "clinic_name": "Happy Paws Veterinary Clinic",
  "license_number": "CLINIC-54321",
  "address": "123 Main Street, San Francisco, CA 94102",
  "is_verified": false,
  "is_active": true,
  "created_at": "2025-10-01T10:00:00"
}
```

#### Get My Clinic Profile

```bash
GET /api/v1/clinic-profiles/me
```

#### Update My Clinic Profile

```bash
PUT /api/v1/clinic-profiles/me

{
  "phone": "+1-415-555-9999",
  "operating_hours": {
    "sunday": "10:00 AM - 2:00 PM"
  }
}
```

#### Search Clinics (Public)

```bash
GET /api/v1/clinic-profiles?clinic_name=Happy&is_verified=true
```

---

### 3. Doctor-Clinic Association Management

#### Create Association (Clinic Owner Adds Doctor)

```bash
POST /api/v1/doctor-clinic-associations/

# Called by clinic owner to add a doctor to their clinic
```

**Request:**
```json
{
  "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
  "clinic_id": "223e4567-e89b-12d3-a456-426614174000",
  "employment_type": "full_time"
}
```

**Response:**
```json
{
  "id": "323e4567-e89b-12d3-a456-426614174000",
  "doctor_id": "123e4567-e89b-12d3-a456-426614174000",
  "clinic_id": "223e4567-e89b-12d3-a456-426614174000",
  "employment_type": "full_time",
  "is_active": true,
  "joined_at": "2025-10-01T10:00:00"
}
```

#### Get All Doctors at a Clinic

```bash
GET /api/v1/doctor-clinic-associations/clinic/{clinic_id}/doctors
```

#### Get All Clinics a Doctor Works At

```bash
GET /api/v1/doctor-clinic-associations/doctor/{doctor_id}/clinics
```

#### Update Association

```bash
PUT /api/v1/doctor-clinic-associations/{association_id}

{
  "employment_type": "part_time"
}
```

#### Delete Association

```bash
DELETE /api/v1/doctor-clinic-associations/{association_id}
```

---

## 🔄 **Complete Workflow Examples**

### Scenario 1: Doctor Joins the System

```bash
#!/bin/bash

# Step 1: Doctor signs up
echo "Step 1: Doctor signing up..."
SIGNUP_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dr.smith@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "+1-415-555-1234",
    "roles": ["doctor"]
  }')

AUTH_TOKEN=$(echo $SIGNUP_RESPONSE | jq -r '.access_token')
echo "✅ User account created, got auth token"

# Step 2: Doctor creates their profile
echo "Step 2: Creating doctor profile..."
PROFILE_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/doctor-profiles/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "license_number": "VET-12345",
    "specialization": "General Practice",
    "years_of_experience": 5,
    "qualifications": [
      {
        "degree": "DVM",
        "institution": "UC Davis",
        "year": 2018
      }
    ],
    "bio": "Passionate about animal care"
  }')

DOCTOR_ID=$(echo $PROFILE_RESPONSE | jq -r '.id')
echo "✅ Doctor profile created: $DOCTOR_ID"

# Step 3: Search for clinics to join
echo "Step 3: Searching for clinics..."
curl -s -X GET "$API_URL/api/v1/clinic-profiles?is_verified=true" \
  -H "Authorization: Bearer $AUTH_TOKEN" | jq '.'

echo "✅ Doctor can now request to join clinics!"
```

### Scenario 2: Clinic Owner Sets Up

```bash
#!/bin/bash

# Step 1: Clinic owner signs up
echo "Step 1: Clinic owner signing up..."
SIGNUP_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@happypaws.com",
    "password": "SecurePass123!",
    "first_name": "Jane",
    "last_name": "Doe",
    "phone": "+1-415-555-5678",
    "roles": ["clinic_owner"]
  }')

AUTH_TOKEN=$(echo $SIGNUP_RESPONSE | jq -r '.access_token')
echo "✅ User account created"

# Step 2: Clinic owner creates clinic profile
echo "Step 2: Creating clinic profile..."
CLINIC_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/clinic-profiles/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "clinic_name": "Happy Paws Veterinary Clinic",
    "license_number": "CLINIC-54321",
    "address": "123 Main Street, SF, CA 94102",
    "phone": "+1-415-555-0123",
    "email": "contact@happypaws.com",
    "operating_hours": {
      "monday": "9AM-6PM",
      "tuesday": "9AM-6PM"
    },
    "services_offered": ["Checkups", "Surgery", "Emergency"]
  }')

CLINIC_ID=$(echo $CLINIC_RESPONSE | jq -r '.id')
echo "✅ Clinic profile created: $CLINIC_ID"

# Step 3: Search for doctors to add
echo "Step 3: Searching for doctors..."
DOCTORS=$(curl -s -X GET "$API_URL/api/v1/doctor-profiles?is_verified=true" \
  -H "Authorization: Bearer $AUTH_TOKEN")

DOCTOR_ID=$(echo $DOCTORS | jq -r '.[0].id')

# Step 4: Add doctor to clinic
echo "Step 4: Adding doctor to clinic..."
curl -s -X POST "$API_URL/api/v1/doctor-clinic-associations/" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": "'"$DOCTOR_ID"'",
    "clinic_id": "'"$CLINIC_ID"'",
    "employment_type": "full_time"
  }' | jq '.'

echo "✅ Clinic fully set up with doctors!"
```

---

## 🎯 **Why This Matters**

### Without Profile Setup:

```
❌ Doctor cannot create medical records
   → doctor_profiles.id doesn't exist
   → medical_records.doctor_id foreign key fails

❌ Clinic cannot be referenced in records
   → clinic_profiles.id doesn't exist
   → medical_records.clinic_id foreign key fails

❌ Cannot verify doctor-clinic relationship
   → No association record
   → Cannot validate if doctor works at clinic
```

### With Profile Setup:

```
✅ Doctor can create medical records
✅ Clinic can be referenced in visits
✅ Doctor-clinic relationship verified
✅ OTP workflow can grant clinic access
✅ Complete audit trail maintained
```

---

## 📊 **Data Flow Diagram**

```
User Signup (POST /auth/signup)
    ↓
users table entry created
    ↓
    ├─→ If role = "doctor"
    │       ↓
    │   POST /doctor-profiles/
    │       ↓
    │   doctor_profiles entry created
    │       ↓
    │   Doctor searches for clinics
    │       ↓
    │   Clinic owner creates association
    │       ↓
    │   doctor_clinic_associations entry
    │       ↓
    │   ✅ Doctor can now create medical records!
    │
    └─→ If role = "clinic_owner"
            ↓
        POST /clinic-profiles/
            ↓
        clinic_profiles entry created
            ↓
        Clinic owner searches for doctors
            ↓
        Creates doctor-clinic associations
            ↓
        ✅ Clinic ready to receive pets!
```

---

## 🔐 **Permission Rules**

### Doctor Profiles
- **Create**: Only by user with `doctor` role for themselves
- **Read Own**: Any authenticated doctor
- **Read Others**: Any authenticated user (public directory)
- **Update Own**: Only the doctor themselves
- **Delete**: Not allowed (deactivate instead)

### Clinic Profiles
- **Create**: Only by user with `clinic_owner` role for themselves
- **Read**: Public (anyone can search clinics)
- **Update Own**: Only the clinic owner
- **Delete**: Not allowed (deactivate instead)

### Doctor-Clinic Associations
- **Create**: Only clinic owner can add doctors
- **Read**: Doctor or clinic owner
- **Update**: Clinic owner or doctor (mutual agreement)
- **Delete**: Clinic owner or doctor (either can end)

---

## ❓ **FAQ**

### Q: Can a user be both a doctor and clinic owner?
**A:** Yes! They have both roles in `users.roles` array, and can create both profiles.

### Q: What if a doctor works at multiple clinics?
**A:** Multiple `doctor_clinic_associations` records with different `clinic_id` values.

### Q: Can a doctor create medical records without a profile?
**A:** No! The `medical_records.doctor_id` foreign key requires a `doctor_profiles.id` to exist.

### Q: What happens if a doctor leaves a clinic?
**A:** The association is marked `is_active = false`. Historical medical records remain unchanged.

### Q: Can pet owners see which doctors work at a clinic?
**A:** Yes, via `GET /doctor-clinic-associations/clinic/{clinic_id}/doctors` (public info).

---

## 🎯 **Next Steps**

1. ✅ **Routes created** (this guide)
2. ⏳ **Implement controllers** (business logic)
3. ⏳ **Implement services** (access control)
4. ⏳ **Add validation** (Pydantic schemas exist)
5. ⏳ **Add tests** (integration tests)
6. ⏳ **Update main.py** (register new routes)

---

## 💡 **Quick Reference**

| Endpoint | Method | Purpose | Who Can Call |
|----------|--------|---------|--------------|
| `/doctor-profiles/` | POST | Create doctor profile | Doctor (self) |
| `/doctor-profiles/me` | GET | Get my profile | Doctor (self) |
| `/doctor-profiles/me` | PUT | Update my profile | Doctor (self) |
| `/doctor-profiles/` | GET | Search doctors | Anyone |
| `/clinic-profiles/` | POST | Create clinic profile | Clinic owner (self) |
| `/clinic-profiles/me` | GET | Get my profile | Clinic owner (self) |
| `/clinic-profiles/me` | PUT | Update my profile | Clinic owner (self) |
| `/clinic-profiles/` | GET | Search clinics | Anyone (public) |
| `/doctor-clinic-associations/` | POST | Add doctor to clinic | Clinic owner |
| `/doctor-clinic-associations/clinic/{id}/doctors` | GET | List clinic doctors | Anyone |
| `/doctor-clinic-associations/doctor/{id}/clinics` | GET | List doctor's clinics | Anyone |

---

**Now you have the complete picture of how doctors and clinics complete their registration!** 🎉

