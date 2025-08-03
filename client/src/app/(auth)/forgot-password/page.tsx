'use client';

import ParentLayout from '@/components/layout/ParentLayout';
import Input from '@/components/ui/Input';
import React, { useState } from 'react';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setIsLoading(true);

    try {
      console.log('Sending OTP to:', email);
    } catch (error) {
      console.error('Error sending OTP:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ParentLayout>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="text-center space-y-5">
          <div className="w-[5rem] rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <img
              src="/group-1.svg"
              alt="TM Logo"
              className="object-contain"
            />
          </div>
          <div className="space-y-2">
            <p className="text-gray-600">Forgot Password</p>
          </div>
        </div>

        <Input
          label="Email address"
          placeholder="Enter your email address"
          buttonType="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full border-gray-200/80 bg-accent-pastel/40 p-2 backdrop-blur-sm focus:border-primary focus:ring-primary/20 placeholder:text-gray-400 outline-none"
        />

        <button
          type="submit"
          disabled={isLoading || !email}
          className="w-full py-3 px-4 rounded-lg font-semibold text-white transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none bg-gradient-to-r from-primary to-primary/90 hover:shadow-lg hover:shadow-primary/25 cursor-pointer"
        >
          {isLoading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>verifying</span>
            </div>
          ) : (
            'Verify email'
          )}
        </button>
      </form>
    </ParentLayout>
  );
};

export default ForgotPassword;
