'use client';

import React, { useState } from 'react';
import { Save } from 'lucide-react';
import Input from '@/components/ui/Input';

interface ProfileData {
  fullName: string;
  email: string;
  phone: string;
  address: string;
}

const ProfileSettings: React.FC = () => {
  const [formData, setFormData] = useState<ProfileData>({
    fullName: '',
    email: '',
    phone: '',
    address: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    console.log('Profile data:', formData);
    // Add your API call here
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-text-primary mb-2">Profile Settings</h2>
        <p className="text-text-secondary">Update your personal information and profile details</p>
      </div>
      
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input
            label="Full Name"
            buttonType="text"
            name="fullName"
            value={formData.fullName}
            onChange={handleInputChange}
            placeholder="Enter your full name"
          />
          
          <Input
            label="Email Address"
            buttonType="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="your.email@example.com"
          />
          
          <Input
            label="Phone Number"
            buttonType="tel"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            placeholder="+91 XXXXX XXXXX"
          />
          
          <Input
            label="Address"
            buttonType="text"
            name="address"
            value={formData.address}
            onChange={handleInputChange}
            placeholder="Your address"
          />
        </div>
        
        <div className="flex justify-end pt-4">
          <button
            onClick={handleSubmit}
            className="flex items-center gap-2 px-6 py-2.5 bg-secondary text-white rounded-lg hover:opacity-90 transition-all shadow-teal"
          >
            <Save size={18} />
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfileSettings;