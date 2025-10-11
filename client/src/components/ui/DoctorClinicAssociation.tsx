import React, { useState } from 'react';
import { Link2 } from 'lucide-react';
import { CustomSelect } from '@/components/ui/CustomSelect';

interface AssociationData {
  doctor_id: string;
  clinic_id: string;
  employment_type: string;
}

const DoctorClinicAssociation: React.FC = () => {
  const [formData, setFormData] = useState<AssociationData>({
    doctor_id: '',
    clinic_id: '',
    employment_type: '',
  });

  // Mock options - replace with actual API calls
  const doctorOptions = [
    { value: 'cd3174c6-c3c2-4c21-b69b-abfbf0c1ffec', label: 'Dr. John Doe - Surgery' },
    { value: 'doctor-2-id', label: 'Dr. Jane Smith - Dentistry' },
  ];

  const clinicOptions = [
    { value: 'a47f2e78-408e-48b8-b40f-d870dc14848c', label: 'Woofzoo Clinic' },
    { value: 'clinic-2-id', label: 'PawCare Center' },
  ];

  const employmentOptions = [
    { value: 'full_time', label: 'Full Time' },
    { value: 'part_time', label: 'Part Time' },
    { value: 'contract', label: 'Contract' },
    { value: 'consultant', label: 'Consultant' },
  ];

  const handleSelectChange = (e: { target: { name: string; value: string } }) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    console.log('Association data:', formData);
    // Add your API call here
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-text-primary mb-2">Doctor-Clinic Association</h2>
        <p className="text-text-secondary">Link a doctor with a clinic and define employment type</p>
      </div>
      
      <div className="space-y-6">
        <div className="grid grid-cols-1 gap-6">
          <CustomSelect
            label="Select Doctor"
            name="doctor_id"
            value={formData.doctor_id}
            options={doctorOptions}
            onChange={handleSelectChange}
            placeholder="Choose a doctor"
          />
          
          <CustomSelect
            label="Select Clinic"
            name="clinic_id"
            value={formData.clinic_id}
            options={clinicOptions}
            onChange={handleSelectChange}
            placeholder="Choose a clinic"
          />
          
          <CustomSelect
            label="Employment Type"
            name="employment_type"
            value={formData.employment_type}
            options={employmentOptions}
            onChange={handleSelectChange}
            placeholder="Select employment type"
          />
        </div>
        
        <div className="flex justify-end pt-4">
          <button
            onClick={handleSubmit}
            className="flex items-center gap-2 px-6 py-2.5 bg-primary text-white rounded-lg hover:opacity-90 transition-all shadow-teal"
          >
            <Link2 size={18} />
            Create Association
          </button>
        </div>
      </div>
    </div>
  );
};

export default DoctorClinicAssociation;