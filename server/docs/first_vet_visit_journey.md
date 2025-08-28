# User Journey: Non-onboarded User's First Vet Visit

## Scenario Overview
**User:** Pet owner who has never used the system before
**Trigger:** Pet needs medical attention, owner visits vet clinic
**Goal:** Create pet profile, provide medical care, onboard owner to system

---

## Journey Steps

### Phase 1: Arrival & Check-in

#### **Step 1: Owner arrives at clinic**
- **Actor:** Pet Owner
- **Action:** Walks into vet clinic with pet
- **Mindset:** Focused on pet's health, unaware of the record system
- **Pain Points:** May be stressed about pet's condition

#### **Step 2: Receptionist initiates check-in**
- **Actor:** Receptionist
- **Action:** Asks for owner's phone number and basic pet information
- **System Action:** Checks if phone number exists in system
- **Result:** Phone number not found → New user flow triggered

### Phase 2: Profile Creation

#### **Step 3: Pet & Owner profile creation**
- **Actor:** Receptionist
- **Action:** Creates new profiles in system
- **Information Collected:**
  - Owner: Name, phone number (primary), address
  - Pet: Name, breed, age, gender, weight, any known medical history
- **System Action:** 
  - Generates unique Pet ID (numerical)
  - Creates owner account with phone as primary identifier
  - Links pet to owner profile

#### **Step 4: Pet ID assignment**
- **Actor:** System
- **Action:** Generates unique Pet ID
- **Result:** Pet ID created (e.g., PET-123456)

### Phase 3: Appointment & Medical Care

#### **Step 5: Appointment scheduling**
- **Actor:** Receptionist
- **Action:** Schedules appointment in system
- **System Action:** Pet added to vet's queue with basic profile information

#### **Step 6: Vet examines pet**
- **Actor:** Vet
- **Action:** Accesses pet profile from queue
- **Available Info:** Basic pet details entered by receptionist
- **System Access:** Full medical record interface (currently blank)

#### **Step 7: Medical record creation**
- **Actor:** Vet  
- **Action:** Adds first medical records
- **Records Include:**
  - Diagnosis
  - Treatment provided
  - Prescriptions/medications
  - Follow-up instructions
  - Any test results
- **System Action:** Creates baseline medical history

### Phase 4: Owner Notification & Onboarding

#### **Step 8: Payment & checkout**
- **Actor:** Receptionist
- **Action:** Processes payment, provides receipt
- **Additional Action:** Informs owner about the pet record system

#### **Step 9: Pet ID delivery via SMS**
- **Actor:** System (Automated)
- **Trigger:** Appointment completion
- **SMS Content:**
  - "Your pet [Pet Name] has been registered in our medical system"
  - "Pet ID: PET-123456"
  - "Download our app to access medical records: [App Store Link]"
  - "Use your phone number [XXX-XXX-XXXX] to log in"

### Phase 5: Owner Self-Onboarding (Optional)

#### **Step 10: Owner downloads app**
- **Actor:** Pet Owner (at home)
- **Action:** Downloads app using link from SMS
- **System Action:** App installation

#### **Step 11: Account access**
- **Actor:** Pet Owner
- **Action:** Opens app, enters phone number
- **System Action:** Sends OTP for verification
- **Result:** Owner gains access to pet's medical records

#### **Step 12: Profile completion (Optional)**
- **Actor:** Pet Owner
- **Action:** Completes pet profile with additional details
- **Possible Additions:**
  - Pet photos
  - Emergency contacts
  - Insurance information
  - Daily journal entries

---

## Success Criteria

### Immediate Success (Clinic Visit)
- ✅ Pet profile created successfully
- ✅ Medical records documented
- ✅ Pet ID generated and communicated
- ✅ Owner informed about system

### Long-term Success (Post-visit)
- ✅ Owner receives and acknowledges Pet ID
- ✅ Owner downloads app (conversion metric)
- ✅ Owner successfully logs in
- ✅ Medical records accessible for future vet visits

---

## Key Touchpoints & Systems

### For Receptionist
- **System Interface:** Pet registration form, appointment scheduling
- **Required Info:** Owner phone, basic pet details
- **Success Measure:** Profile created without errors

### For Vet
- **System Interface:** Medical records entry, prescription management
- **Available Data:** Pet profile, previous records (none for first visit)
- **Success Measure:** Complete medical documentation

### For Pet Owner
- **Touchpoints:** SMS notification, app download, profile access
- **Success Measure:** Successful app login and record access

---

## Potential Pain Points & Solutions

### Pain Point 1: Owner doesn't understand the system
**Solution:** Receptionist brief explanation + informational brochure

### Pain Point 2: Owner doesn't receive SMS
**Solution:** Backup notification via email or physical card with Pet ID

### Pain Point 3: Owner doesn't download app
**Solution:** Follow-up SMS after 48 hours with benefits explanation

### Pain Point 4: Technical difficulties during profile creation
**Solution:** Offline backup form, sync when system available

---

## Next Steps After This Journey

1. **Future vet visits** will use Scenario B (existing user with Pet ID)
2. **Family member addition** can be done through the app
3. **Daily journaling** becomes available through the app
4. **Emergency access** possible via Pet ID on physical tag