# Technical Requirements Document (TRD) for Pet Medical Record System

## 1. Introduction

### 1.1 Purpose
This Technical Requirements Document (TRD) defines the technical specifications for a pet medical record system designed to support two primary user journeys:
- **First Vet Visit**: Onboarding new pet owners, creating pet profiles, and initiating medical records.
- **Existing User Visiting New Vet**: Enabling seamless sharing of pet medical history with new clinics, with secure access control.

The system supports pet owners, family members, veterinarians, and clinics, ensuring scalable and efficient management of pet data and medical records. It includes features for vet-to-clinic associations, doctor assignment per visit, and time-limited access control.

### 1.2 Scope
The system provides:
- Pet profile creation and management for owners and authorized family members.
- Access to medical history for owners, family members, and assigned vets.
- Assignment of a vet to a pet during clinic visits, with access expiring after one month unless the clinic is trusted.
- Scalable storage and retrieval of pet data and medical history, with monthly partitioning for access records.
- OTP-based authentication and notification delivery via SMS.

### 1.3 Stakeholders
- **Pet Owners**: Create and access pet profiles, share with family, receive visit summaries.
- **Family Members**: Access pet data with configurable permissions (e.g., read-only).
- **Receptionists**: Handle check-in, OTP validation, appointment scheduling.
- **Vets**: Access medical history and add records, tied to assigned visits.
- **Clinics**: Gain trusted status for streamlined access to pet records.

## 2. System Overview

### 2.1 Objective
The pet medical record system aims to provide a robust platform for:
- Creating and managing pet profiles with details like name, breed, age, and owner-added data (e.g., photos, journal entries).
- Maintaining an immutable medical history timeline for each pet, accessible to authorized stakeholders.
- Assigning vets to pet visits, with access control limited to the assigned vet for one month.
- Supporting scalability for millions of pets and medical records, with efficient search and sharing mechanisms.

### 2.2 Key Features
- **Pet Profile Management**: Create, update, and share pet profiles.
- **Medical Record Management**: Add, retrieve, and search immutable medical records.
- **Access Control**: OTP-based authentication for new clinics; assigned vet access; trusted clinic status.
- **Notifications**: SMS delivery for OTPs, Pet IDs, and visit summaries.
- **Appointment Scheduling**: Manage vet visit queues and assignments.

## 3. Functional Requirements

### 3.1 Pet Profile Management
- **Create Profile**:
  - API: `POST /owners`, `POST /pets`
  - Inputs: Owner (phone, name, email, address), Pet (name, breed, age, gender, weight, photos, insurance).
  - Output: Generates unique `pet_id` (e.g., "PET-123456").
- **Update Profile**:
  - API: `PATCH /pets/{pet_id}`
  - Allows owners/family to add photos, emergency contacts, journal entries.
- **Share Profile**:
  - API: `POST /pets/{pet_id}/share`
  - Owners add family members via phone number, validated by OTP.

### 3.2 Medical Record Management
- **Create Records**:
  - API: `POST /pets/{pet_id}/records`
  - Inputs: Diagnosis, treatment, prescriptions (JSON), test results (JSON/URLs), follow-up instructions.
  - Enforced immutability: Records cannot be edited, only appended.
- **Retrieve Records**:
  - API: `GET /pets/{pet_id}/records?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
  - Paginated, filtered by date, retrieved directly from database.
- **Search Records**:
  - API: `GET /pets/{pet_id}/records/search?q=query`
  - Full-text search on diagnosis/treatment fields using PostgreSQL `tsvector`.

### 3.3 Access Control
- **OTP Authentication**:
  - API: `POST /otp/generate`, `POST /otp/validate`
  - Generates 6-digit OTP, sent via SMS, valid for 10 minutes, max 3 attempts.
- **Doctor Assignment**:
  - API: `POST /pet_clinic_access`
  - Assigns a vet to a pet for a clinic visit, stored in `pet_clinic_access` table.
  - Access limited to assigned vet for one month unless clinic is trusted.
- **Trusted Clinics**:
  - API: `POST /trusted_clinics`
  - Grants ongoing access to clinics, optionally with expiration.

### 3.4 Notifications
- **SMS Notifications**:
  - API: `POST /notifications/sms`
  - Types: OTP, Pet ID delivery, visit summary.
  - Content: Includes pet name, clinic name, app link (if applicable).
- **Visit Summary**:
  - Sent post-visit with new records, prescriptions, and follow-up instructions.

### 3.5 Appointment Scheduling
- **Schedule Appointment**:
  - API: `POST /appointments`
  - Inputs: Pet ID, clinic ID, vet ID (optional), appointment time.
- **Queue Management**:
  - API: `GET /clinics/{clinic_id}/queue`
  - Displays pets in queue with basic details and assigned vet.

## 4. Non-Functional Requirements

### 4.1 Performance
- **Pet Lookup**: <2 seconds (direct database query).
- **OTP Delivery**: <30 seconds (via external SMS provider).
- **Medical History Load**: <3 seconds (paginated results from database).
- **Record Updates**: Saved immediately (synchronous writes).
- **Query Latency**: Optimize with database indexes.

### 4.2 Scalability
- Support 10M pets, 100M medical records, 1M monthly visits.
- Partition `medical_records` by `visit_date` (yearly).
- Partition `pet_clinic_access` by `access_date` (monthly).

### 4.3 Reliability
- **Uptime**: 99.9% for application and database.
- **Assumption**: Clinics have reliable internet; no offline mode required.

### 4.4 Logging
- Logs stored in **AWS CloudWatch** with a configurable retention period (e.g., 7 days).
- Log all API requests, database queries, and errors for debugging.

### 4.5 User Experience
- Clear error messages for failed actions (e.g., invalid OTP).
- Progress indicators for OTP delivery, record loading.
- Mobile app with timeline view, date filters, and search functionality.

## 5. Data Model

### 5.1 Tables
1. **Owners**:
   - Fields: `owner_id` (UUID, PK), `phone_number` (VARCHAR, Unique), `name` (VARCHAR), `email` (VARCHAR), `address` (TEXT), `created_at`, `updated_at` (TIMESTAMP).
   - Indexes: `phone_number`.
2. **Pets**:
   - Fields: `pet_id` (VARCHAR, PK, e.g., "PET-123456"), `owner_id` (FK), `name` (VARCHAR), `breed` (VARCHAR), `age` (INTEGER), `gender` (ENUM), `weight` (FLOAT), `photos` (JSONB), `emergency_contacts` (JSONB), `insurance_info` (JSONB), `created_at`, `updated_at`.
   - Indexes: `owner_id`.
3. **Family_Members**:
   - Fields: `family_member_id` (UUID, PK), `owner_id` (FK), `pet_id` (FK), `phone_number` (VARCHAR, Unique), `name` (VARCHAR), `access_level` (ENUM: Full, Read-Only), `created_at`, `updated_at`.
   - Indexes: `pet_id`.
4. **Clinics**:
   - Fields: `clinic_id` (UUID, PK), `name` (VARCHAR), `address` (TEXT), `phone_number` (VARCHAR), `created_at`.
5. **Vets**:
   - Fields: `vet_id` (UUID, PK), `name` (VARCHAR), `license_number` (VARCHAR), `created_at`.
6. **Vet_Clinics**:
   - Fields: `vet_clinic_id` (UUID, PK), `vet_id` (FK), `clinic_id` (FK), `created_at`.
   - Indexes: `vet_id`, `clinic_id`.
   - Constraint: `UNIQUE(vet_id, clinic_id)`.
7. **Medical_Records**:
   - Fields: `record_id` (UUID, PK), `pet_id` (FK), `vet_id` (FK), `clinic_id` (FK), `visit_date` (TIMESTAMP), `diagnosis` (TEXT), `treatment` (TEXT), `prescriptions` (JSONB), `test_results` (JSONB), `follow_up_instructions` (TEXT), `created_at`, `created_by` (FK).
   - Partitioned by: `visit_date` (yearly, e.g., `medical_records_2025`).
   - Indexes: `pet_id`, `visit_date`.
8. **Pet_Clinic_Access**:
   - Fields: `access_id` (UUID, PK), `pet_id` (FK), `clinic_id` (FK), `vet_id` (FK), `access_date` (TIMESTAMP), `status` (ENUM: Active, Expired), `created_at`.
   - Partitioned by: `access_date` (monthly, e.g., `pet_clinic_access_2025_01`).
   - Indexes: `pet_id`, `access_date`.
9. **OTP**:
   - Fields: `otp_id` (UUID, PK), `pet_id` (FK), `phone_number` (VARCHAR), `otp_code` (VARCHAR), `clinic_id` (FK), `expires_at` (TIMESTAMP), `status` (ENUM: Pending, Used, Expired), `created_at`.
   - Indexes: `otp_code`.
10. **Trusted_Clinics**:
    - Fields: `trusted_id` (UUID, PK), `pet_id` (FK), `clinic_id` (FK), `granted_at`, `expires_at` (TIMESTAMP).
    - Indexes: `pet_id`.
11. **Audit_Logs**:
    - Fields: `log_id` (UUID, PK), `pet_id` (FK), `user_id` (UUID), `action` (VARCHAR), `timestamp`.

### 5.2 Partitioning Strategy
- **Medical_Records**: Range partitioned by `visit_date` (yearly) to optimize timeline queries.
- **Pet_Clinic_Access**: Range partitioned by `access_date` (monthly) for efficient retrieval.
- **Expiration**: `pet_clinic_access` records marked `Expired` or dropped after one month via a scheduled job (e.g., cron).

### 5.3 Storage
- **PostgreSQL**: Core tables for structured data (owners, pets, access, etc.).
- **Amazon S3**: Test results, images (stored with URLs in `medical_records.test_results`).

## 6. System Architecture

### 6.1 Monolithic Architecture
The system is implemented as a **monolithic application** to simplify development and deployment in the initial phase:
- **Application Layer**: A single application handles all functionality (profile management, medical records, access control, notifications, appointments).
  - Framework: Suggested options include Spring Boot (Java), Django (Python), or Ruby on Rails.
  - APIs: RESTful endpoints for all operations (e.g., `/pets`, `/records`, `/otp`, `/appointments`).
- **Database Layer**: PostgreSQL for structured data; S3 for large files (e.g., test results, images).
- **Logging**: AWS CloudWatch for request/errors logs, with a retention period (e.g., 7 days).

### 6.2 Workflow Example (Existing User, New Vet Visit)
1. Owner provides `pet_id` and `phone_number` at clinic.
2. Receptionist calls `GET /pets/{pet_id}/lookup` (PostgreSQL query).
3. System generates OTP (`POST /otp/generate`, stored in PostgreSQL, sent via Twilio).
4. Receptionist validates OTP (`POST /otp/validate`).
5. Vet assigned via `POST /pet_clinic_access` (stored in monthly partition).
6. Vet retrieves records (`GET /pets/{pet_id}/records`, PostgreSQL/S3).
7. Vet adds new record (`POST /pets/{pet_id}/records`).
8. System sends visit summary SMS (`POST /notifications/sms`).
9. Actions logged in CloudWatch and `audit_logs` table.

## 7. Edge Cases
- **Forgotten Pet ID**: Lookup by `phone_number` + `pet_name` with verification questions (e.g., last visit date).
- **OTP Not Received**: Resend option (max 3 attempts); fallback to app login or manual verification.
- **Phone Number Changed**: Update via app with OTP sent to old and new numbers.
- **Multiple Pets**: Display pet list (name, breed) in UI for selection.

## 8. Assumptions
- System handles 10M pets, 100M medical records, 1M monthly visits.
- SMS delivery via third-party provider (e.g., Twilio).
- Clinics have reliable internet; no offline mode required.
- Compliance with data privacy regulations (e.g., GDPR, CCPA).

## 9. Constraints
- Medical records are immutable.
- `pet_clinic_access` data expires after one month.
- OTPs expire after 10 minutes; max 3 failed attempts.
- Audit logging required for all record access.

## 10. Risks and Mitigation
- **Scalability**: Mitigated by partitioning (`medical_records`, `pet_clinic_access`) and database indexing.
- **Data Consistency**: Use database transactions for critical updates (e.g., profile creation, record addition).
- **Large Files**: Store test results/images in S3, reference via URLs in `medical_records`.
- **Performance**: Optimize queries with indexes; monitor via CloudWatch.

## 11. Success Criteria
- **Immediate**:
  - Successful pet profile lookup and OTP validation.
  - Complete medical history accessible to assigned vet.
  - New records added without errors.
  - Owners receive visit summaries and can access records.
- **Long-term**:
  - Medical history remains continuous and accessible.
  - Streamlined future visits for trusted clinics.
  - High owner app adoption and login success rate.