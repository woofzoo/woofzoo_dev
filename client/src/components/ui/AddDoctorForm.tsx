import React, { useState } from 'react';
import { UserPlus } from 'lucide-react';
import Input from '@/components/ui/Input';
import { CustomSelect } from '@/components/ui/CustomSelect';

interface DoctorData {
  license_number: string;
  specialization: string;
  user_id: string;
  years_of_experience: number;
  qualifications: {
    [key: string]: string;
  };
  bio: string;
}

const AddDoctorForm: React.FC = () => {
  const [formData, setFormData] = useState<DoctorData>({
    license_number: '',
    specialization: '',
    user_id: '',
    years_of_experience: 0,
    qualifications: {
      MD: '',
      MBBS: '',
    },
    bio: '',
  });

  // Mock user options - replace with actual API call
  const userOptions = [
    { value: '69f71c71-9157-43d2-844a-6c6eb23d1d81', label: 'Dr. John Doe' },
    { value: 'user-2-id', label: 'Dr. Jane Smith' },
    { value: 'user-3-id', label: 'Dr. Mike Johnson' },
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    
    if (name === 'years_of_experience') {
      setFormData({
        ...formData,
        [name]: parseInt(value) || 0
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSelectChange = (e: { target: { name: string; value: string } }) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleQualificationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      qualifications: {
        ...formData.qualifications,
        [name]: value
      }
    });
  };

  const handleSubmit = async () => {
    console.log('Doctor data:', formData);
    // Add your API call here
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-text-primary mb-2">Add Doctor</h2>
        <p className="text-text-secondary">Register a new veterinary doctor to the system</p>
      </div>
      
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <CustomSelect
            label="Select User/Doctor"
            name="user_id"
            value={formData.user_id}
            options={userOptions}
            onChange={handleSelectChange}
            placeholder="Select doctor"
          />
          
          <Input
            label="License Number"
            buttonType="text"
            name="license_number"
            value={formData.license_number}
            onChange={handleInputChange}
            placeholder="VET-12345"
          />
          
          <Input
            label="Specialization"
            buttonType="text"
            name="specialization"
            value={formData.specialization}
            onChange={handleInputChange}
            placeholder="e.g., Surgery, Small Animals"
          />
          
          <Input
            label="Years of Experience"
            buttonType="number"
            name="years_of_experience"
            value={formData.years_of_experience.toString()}
            onChange={handleInputChange}
            placeholder="0"
          />

          <Input
            label="MD Qualification"
            buttonType="text"
            name="MD"
            value={formData.qualifications.MD}
            onChange={handleQualificationChange}
            placeholder="MD from CA"
          />

          <Input
            label="MBBS Qualification"
            buttonType="text"
            name="MBBS"
            value={formData.qualifications.MBBS}
            onChange={handleQualificationChange}
            placeholder="MBBS from AIIMS"
          />

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-text-primary mb-2">Bio</label>
            <textarea
              name="bio"
              value={formData.bio}
              onChange={handleInputChange}
              rows={4}
              className="w-full border border-border-primary rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-pastel"
              placeholder="Enter doctor's bio"
            />
          </div>
        </div>
        
        <div className="flex justify-end pt-4">
          <button
            onClick={handleSubmit}
            className="flex items-center gap-2 px-6 py-2.5 bg-secondary text-white rounded-lg hover:opacity-90 transition-all shadow-teal"
          >
            <UserPlus size={18} />
            Add Doctor
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddDoctorForm;