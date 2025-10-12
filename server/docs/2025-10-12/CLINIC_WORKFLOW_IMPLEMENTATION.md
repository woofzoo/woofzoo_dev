# Clinic Workflow & Doctor Queue Implementation

## Status: IN PROGRESS 🚧

### ✅ Phase 1 Complete: Clinic Workflow

1. **Database Migration** ✅
   - ✅ New `QueueStatus` enum (pending_precheck, ready_for_doctor, with_doctor, completed)
   - ✅ Pre-check vital fields (weight, temperature, heart_rate, respiratory_rate, notes)
   - ✅ Queue management fields (queue_status, queue_position, assigned_to_doctor_at, visit_completed_at)
   - ✅ Medical record link field
   - ✅ Migration applied successfully

2. **Model Updates** ✅
   - ✅ Updated `PetClinicAccess` model with new fields
   - ✅ Added `QueueStatus` enum

3. **Schemas** ✅
   - ✅ `app/schemas/clinic_workflow.py` created
   - ✅ PetSearchRequest/Response
   - ✅ OTPRequestData/Response
   - ✅ OTPVerifyRequest/Response
   - ✅ PreCheckVitalsUpdate/Response
   - ✅ AssignDoctorRequest/Response

4. **Repositories** ✅
   - ✅ Created `app/repositories/otp.py`
   - ✅ `PetClinicAccessRepository` already exists

5. **Services** ✅
   - ✅ Created `app/services/clinic_workflow_service.py`
   - ✅ search_pet()
   - ✅ request_otp_for_visit()
   - ✅ verify_otp_and_create_access()
   - ✅ update_pre_check_vitals()
   - ✅ assign_to_doctor()

6. **Email Templates** ✅
   - ✅ Added clinic access OTP email template
   - ✅ Updated `app/services/email.py` with send_clinic_access_otp_email()

7. **Controllers** ✅
   - ✅ Created `app/controllers/clinic_workflow_controller.py`
   - ✅ All 5 endpoints implemented

8. **Routes** ✅
   - ✅ Created `app/routes/clinic_workflow.py`
   - ✅ POST /clinic/pets/search
   - ✅ POST /clinic/access/request-otp
   - ✅ POST /clinic/access/verify-otp
   - ✅ PATCH /clinic/access/{id}/pre-checks
   - ✅ POST /clinic/access/{id}/assign-doctor

9. **Dependencies** ✅
   - ✅ All services, controllers, and repositories wired up
   - ✅ Routes registered in main.py

### 🚧 Phase 2 In Progress: Doctor Queue

10. **Schemas** - Need to create:
   - [ ] `app/schemas/doctor_queue.py` (queue, visits)

4. **Services** - Need to create/update:
   - [ ] `app/services/clinic_workflow_service.py` (pet search)
   - [ ] Update `app/services/clinic_access_service.py` (OTP, pre-checks, assign)
   - [ ] `app/services/doctor_queue_service.py` (queue management)
   - [ ] Add email templates for OTP

5. **Controllers** - Need to create/update:
   - [ ] `app/controllers/clinic_workflow_controller.py`
   - [ ] Update `app/controllers/clinic_access_controller.py`
   - [ ] `app/controllers/doctor_controller.py`

6. **Routes** - Need to create/update:
   - [ ] `app/routes/clinic_workflow.py` or extend `app/routes/clinic_access.py`
   - [ ] `app/routes/doctor.py`
   - [ ] Register routes in `app/main.py`

## Implementation Order

### Phase 1: Clinic Pet Search ✅ Next
- Create clinic workflow schemas
- Create pet search service
- Create clinic workflow controller
- Create clinic workflow routes

### Phase 2: OTP & Pre-Checks
- Extend OTP service for email sending
- Add pre-check update functionality
- Add email template for OTP
- Update clinic access controller

### Phase 3: Doctor Assignment
- Add assign-to-doctor functionality
- Create initial medical record
- Update queue status

### Phase 4: Doctor Queue
- Create doctor queue schemas
- Create doctor queue service
- Create doctor controller
- Create doctor routes

### Phase 5: Visit Completion & History
- Add visit completion logic
- Add visit history for owners
- Test end-to-end workflow

## Files to Create/Modify

### New Files (10+)
1. `app/schemas/clinic_workflow.py`
2. `app/schemas/doctor_queue.py`
3. `app/services/clinic_workflow_service.py`
4. `app/services/doctor_queue_service.py`
5. `app/controllers/clinic_workflow_controller.py`
6. `app/controllers/doctor_controller.py`
7. `app/routes/clinic_workflow.py`
8. `app/routes/doctor.py`

### Modified Files (5+)
1. `app/models/pet_clinic_access.py` ✅
2. `app/services/clinic_access_service.py`
3. `app/services/email.py`
4. `app/templates/email_templates.py`
5. `app/main.py`

## Testing Checklist

- [ ] Clinic can search pet by email
- [ ] Clinic can search pet by phone
- [ ] Clinic can search pet by pet_id
- [ ] OTP sent to correct owner email
- [ ] OTP verification works
- [ ] Pre-check vitals can be updated
- [ ] Pet assigned to doctor's queue
- [ ] Doctor sees today's queue
- [ ] Doctor can update medical records
- [ ] Doctor can complete visit
- [ ] Owner can view visit history

