# User Journey: Existing User Visiting New Vet

## Scenario Overview
**User:** Pet owner who already has pet registered in the system (either self-onboarded or created via previous vet visit)
**Trigger:** Needs to visit a new vet clinic (relocation, emergency, specialist referral, or preference change)
**Goal:** Seamlessly share complete medical history with new vet, receive continued care, add new records

---

## Journey Steps

### Phase 1: Pre-Visit Preparation

#### **Step 1: Owner decides to visit new vet**
- **Actor:** Pet Owner
- **Trigger:** New location, emergency, specialist referral, or switching vets
- **Mindset:** Confident that medical records are available in the system
- **Available Info:** Pet ID (from previous SMS or app)

#### **Step 2: Appointment booking**
- **Actor:** Pet Owner
- **Action:** Calls new vet clinic or books online
- **Information Provided:** Pet ID number and owner's phone number
- **Receptionist Action:** Notes Pet ID and phone number for the appointment

### Phase 2: Arrival & Authentication

#### **Step 3: Arrival at new clinic**
- **Actor:** Pet Owner
- **Action:** Arrives at clinic with pet
- **Brings:** Pet ID (written down, in app, or memorized)

#### **Step 4: Check-in process**
- **Actor:** Receptionist
- **Action:** Requests Pet ID and owner's phone number
- **Owner Provides:** Pet ID: PET-123456, Phone: XXX-XXX-XXXX
- **System Action:** Receptionist enters details to lookup pet profile

#### **Step 5: Profile verification**
- **Actor:** System
- **Action:** Finds pet profile linked to the phone number
- **Display:** Shows basic pet info (name, breed, age) for verification
- **Receptionist:** Confirms pet details with owner

### Phase 3: OTP Validation

#### **Step 6: OTP request**
- **Actor:** System
- **Trigger:** New vet clinic access request
- **Action:** Generates and sends OTP to owner's phone
- **SMS Content:** "Your pet [Pet Name] - OTP for [Clinic Name]: 123456. Valid for 10 minutes."

#### **Step 7: Owner receives OTP**
- **Actor:** Pet Owner
- **Action:** Receives SMS with OTP
- **Display:** Shows OTP on phone screen to receptionist

#### **Step 8: OTP verification**
- **Actor:** Receptionist
- **Action:** Enters OTP into system
- **System Action:** Validates OTP and grants access to pet's medical records
- **Result:** Complete medical history becomes available

### Phase 4: Medical History Access & Appointment

#### **Step 9: Appointment scheduling**
- **Actor:** Receptionist
- **Action:** Schedules appointment with validated pet profile
- **System Action:** Pet added to vet's queue with full medical history access

#### **Step 10: Waiting period**
- **Actor:** Pet Owner
- **Action:** Waits for appointment
- **Advantage:** Confident that vet will have complete medical history

### Phase 5: Veterinary Consultation

#### **Step 11: Vet accesses medical history**
- **Actor:** Vet
- **Action:** Reviews pet's complete medical records from queue
- **Available Information:**
  - Complete vaccination history
  - Previous diagnoses and treatments
  - Current medications
  - Allergies and medical conditions
  - Previous test results and images
  - Recent journal entries by family members

#### **Step 12: Informed consultation**
- **Actor:** Vet
- **Action:** Conducts examination with full medical context
- **Advantage:** No need to repeat medical history questions
- **Owner Experience:** Feels confident vet has complete picture

#### **Step 13: Treatment decision**
- **Actor:** Vet
- **Action:** Makes treatment decisions based on complete medical history
- **Considerations:** Drug interactions, previous treatments, chronic conditions

### Phase 6: Record Updates

#### **Step 14: New medical record entry**
- **Actor:** Vet
- **Action:** Adds new medical records to existing profile
- **New Records Include:**
  - Today's diagnosis
  - Treatment provided
  - New prescriptions
  - Follow-up instructions
  - Any new test results
- **System Restriction:** Cannot edit previous records from other vets

#### **Step 15: Prescription management**
- **Actor:** Vet
- **Action:** Adds new prescriptions
- **System Action:** New prescriptions appear alongside existing medication history
- **Note:** Previous prescriptions remain visible but marked as "Previous" or "From [Other Vet Name]"

### Phase 7: Checkout & Future Access

#### **Step 16: Payment and checkout**
- **Actor:** Receptionist
- **Action:** Processes payment
- **System Update:** Appointment marked as completed

#### **Step 17: Ongoing access establishment**
- **Actor:** System
- **Action:** New vet clinic gains "trusted" status for this pet
- **Result:** Future visits to this clinic won't require OTP (within reasonable timeframe)

### Phase 8: Owner Notification & Follow-up

#### **Step 18: Visit summary notification**
- **Actor:** System (Automated)
- **Action:** Sends SMS to owner
- **SMS Content:** 
  - "Visit completed at [Clinic Name]"
  - "New records added to [Pet Name]'s profile"
  - "View details in app: [App Link]"

#### **Step 19: Owner reviews updates**
- **Actor:** Pet Owner (Optional)
- **Action:** Opens app to review new medical records
- **Available:** New diagnosis, prescriptions, vet notes, follow-up instructions

---

## Success Criteria

### Immediate Success (During Visit)
- ✅ Pet ID and phone number successfully locate profile
- ✅ OTP delivered and validated within time limit
- ✅ Complete medical history accessible to vet
- ✅ New records added without system errors
- ✅ Owner feels confident in care continuity

### Long-term Success (Post-visit)
- ✅ Medical history remains complete and continuous
- ✅ Future visits to this clinic streamlined
- ✅ Owner receives visit summary and can access new records
- ✅ All stakeholders have updated information

---

## Key Touchpoints & Systems

### For Pet Owner
- **Pre-visit:** Has Pet ID ready, confident in system
- **During visit:** Provides Pet ID, receives and shares OTP
- **Post-visit:** Receives updates, can access new records
- **Success Measure:** Seamless experience with complete medical continuity

### For Receptionist
- **System Interface:** Pet lookup, OTP verification, appointment scheduling
- **Required Actions:** Verify pet identity, validate OTP, schedule appointment
- **Success Measure:** Quick verification and scheduling without delays

### For Vet
- **System Interface:** Complete medical history review, new record entry
- **Available Data:** Full medical timeline, current medications, previous treatments
- **Success Measure:** Can make informed decisions with complete medical context

---

## Potential Pain Points & Solutions

### Pain Point 1: Owner forgets Pet ID
**Solution:** Lookup by phone number + pet name + additional verification questions

### Pain Point 2: OTP not received
**Solutions:** 
- Resend OTP option
- Backup verification via app if owner is logged in
- Manual verification with additional identity questions

### Pain Point 3: Phone number changed
**Solution:** Alternative verification through app login or previous vet confirmation

### Pain Point 4: Emergency situations
**Solution:** Emergency override process with post-visit verification

### Pain Point 5: Multiple pets with same owner
**Solution:** Clear pet selection interface showing pet names and basic details

---

## System Requirements

### Security Features
- OTP expires after 10 minutes
- Failed OTP attempts locked after 3 tries
- Audit trail of all record access
- New vet clinic access logged

### Performance Requirements
- Pet lookup response < 2 seconds
- OTP delivery < 30 seconds
- Medical history loads < 3 seconds
- Record updates save immediately

### User Experience Requirements
- Clear error messages for failed verification
- Progress indicators during system operations
- Confirmation messages for successful actions
- Easy-to-read medical history presentation

---

## Edge Cases Handled

1. **Multiple family members present:** Any family member can provide OTP
2. **Clinic system downtime:** Offline mode with sync capability
3. **Pet ownership disputes:** Clear primary owner designation
4. **Specialist referrals:** Referral notes included in accessible history
5. **Emergency after hours:** Emergency access protocols

---

## Integration Points

### With Previous Journey
- Builds on pet profiles created in first-time visit
- Leverages established Pet ID system
- Uses same SMS notification system

### Future Considerations
- Integration with appointment booking systems
- Integration with pharmacy systems for prescriptions
- Integration with lab systems for test results