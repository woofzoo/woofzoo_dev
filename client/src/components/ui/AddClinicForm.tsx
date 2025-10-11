"use client";

import React, { useState } from 'react';
import { Building2 } from 'lucide-react';
import Input from '@/components/ui/Input';
import { CustomSelect } from '@/components/ui/CustomSelect';

interface ClinicData {
  clinic_name: string;
  license_number: string;
  address: string;
  phone: string;
  email: string;
  user_id: string;
  operating_hours: {
    monday: string;
    tuesday: string;
    wednesday: string;
    thursday: string;
    friday: string;
    saturday: string;
    sunday: string;
  };
  services_offered: {
    general_checkup: boolean;
    emergency_care: boolean;
    surgery: boolean;
    grooming: boolean;
  };
}

const AddClinicForm: React.FC = () => {
  const [formData, setFormData] = useState<ClinicData>({
    clinic_name: '',
    license_number: '',
    address: '',
    phone: '',
    email: '',
    user_id: '',
    operating_hours: {
      monday: '9:00 AM - 6:00 PM',
      tuesday: '9:00 AM - 6:00 PM',
      wednesday: '9:00 AM - 6:00 PM',
      thursday: '9:00 AM - 6:00 PM',
      friday: '9:00 AM - 6:00 PM',
      saturday: '10:00 AM - 4:00 PM',
      sunday: 'Closed',
    },
    services_offered: {
      general_checkup: true,
      emergency_care: true,
      surgery: true,
      grooming: false,
    },
  });

  // Mock user options - replace with actual API call
  const userOptions = [
    { value: 'ce6f3e61-b795-423e-8a44-11a23ff06025', label: 'User 1' },
    { value: 'user-2-id', label: 'User 2' },
    { value: 'user-3-id', label: 'User 3' },
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSelectChange = (e: { target: { name: string; value: string } }) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleServiceToggle = (service: keyof ClinicData['services_offered']) => {
    setFormData({
      ...formData,
      services_offered: {
        ...formData.services_offered,
        [service]: !formData.services_offered[service]
      }
    });
  };

  const handleSubmit = async () => {
    console.log('Clinic data:', formData);
    // Add your API call here
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-text-primary mb-2">Add Clinic</h2>
        <p className="text-text-secondary">Register a new veterinary clinic to the system</p>
      </div>
      
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input
            label="Clinic Name"
            buttonType="text"
            name="clinic_name"
            value={formData.clinic_name}
            onChange={handleInputChange}
            placeholder="Enter clinic name"
          />
          
          <Input
            label="License Number"
            buttonType="text"
            name="license_number"
            value={formData.license_number}
            onChange={handleInputChange}
            placeholder="VET-2023-12345"
          />
          
          <Input
            label="Clinic Email"
            buttonType="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="clinic@example.com"
          />
          
          <Input
            label="Clinic Phone"
            buttonType="tel"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            placeholder="+91 XXXXX XXXXX"
          />
          
          <div className="md:col-span-2">
            <Input
              label="Clinic Address"
              buttonType="text"
              name="address"
              value={formData.address}
              onChange={handleInputChange}
              placeholder="Enter complete clinic address"
            />
          </div>

          <div className="md:col-span-2">
            <CustomSelect
              label="Owner/User"
              name="user_id"
              value={formData.user_id}
              options={userOptions}
              onChange={handleSelectChange}
              placeholder="Select clinic owner"
            />
          </div>
        </div>

        {/* Services Offered */}
        <div>
          <h3 className="text-lg font-medium text-text-primary mb-3">Services Offered</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(formData.services_offered).map(([key, value]) => (
              <label key={key} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={value}
                  onChange={() => handleServiceToggle(key as keyof ClinicData['services_offered'])}
                  className="w-4 h-4 text-primary border-border-primary rounded focus:ring-2 focus:ring-primary-pastel"
                />
                <span className="text-sm text-text-primary capitalize">
                  {key.replace(/_/g, ' ')}
                </span>
              </label>
            ))}
          </div>
        </div>
        
        <div className="flex justify-end pt-4">
          <button
            onClick={handleSubmit}
            className="flex items-center gap-2 px-6 py-2.5 bg-secondary text-white rounded-lg hover:opacity-90 transition-all shadow-teal"
          >
            <Building2 size={18} />
            Add Clinic
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddClinicForm;