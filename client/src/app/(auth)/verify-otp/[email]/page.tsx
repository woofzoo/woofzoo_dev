'use client';

import ParentLayout from '@/components/layout/ParentLayout';
import React, { useRef, useState } from 'react';

const VerifyOtp = () => {
   const [otp, setOtp] = useState<string[]>(new Array(6).fill(''));
   const [isLoading, setIsLoading] = useState(false);
   const inputsRef = useRef<(HTMLInputElement | null)[]>([]);

   const handleChange = (index: number, value: string) => {
      if (!/^\d?$/.test(value)) return;

      const updatedOtp = [...otp];
      updatedOtp[index] = value;
      setOtp(updatedOtp);

      // Move to next input
      if (value && index < 5) {
         inputsRef.current[index + 1]?.focus();
      }
   };

   const handleKeyDown = (
      e: React.KeyboardEvent<HTMLInputElement>,
      index: number
   ) => {
      if (e.key === 'Backspace') {
         if (otp[index] === '' && index > 0) {
            const updatedOtp = [...otp];
            updatedOtp[index - 1] = '';
            setOtp(updatedOtp);
            inputsRef.current[index - 1]?.focus();
         }
      } else if (e.key === 'ArrowLeft' && index > 0) {
         inputsRef.current[index - 1]?.focus();
      } else if (e.key === 'ArrowRight' && index < 5) {
         inputsRef.current[index + 1]?.focus();
      }
   };

   const handleSubmit = () => {
      const fullOtp = otp.join('');
      console.log('Submitted OTP:', fullOtp);
      // Add your verification logic here
   };

   return (
      <ParentLayout>
         <div className="space-y-6">
            <div className="text-center space-y-5">
               <div className="w-[5rem] rounded-2xl mx-auto mb-4 flex items-center justify-center">
                  <img
                     src="/group-1.svg"
                     alt="TM Logo"
                     className=" object-contain"
                  />
               </div>
               <div className="space-y-2">
                  <p className="text-gray-600">Verify by entering 6 digit OTP</p>
               </div>
            </div>

            {/* OTP Inputs */}
            <div className="flex justify-between gap-2 max-w-md mx-auto">
               {otp.map((digit, idx) => (
                  <input
                     key={idx}
                     ref={(el) => {
                        inputsRef.current[idx] = el;
                     }}
                     type="text"
                     inputMode="numeric"
                     maxLength={1}
                     value={digit}
                     onChange={(e) => handleChange(idx, e.target.value)}
                     onKeyDown={(e) => handleKeyDown(e, idx)}
                     className="w-12 h-14 rounded-md text-center text-lg border border-gray-300 bg-accent-pastel/40 backdrop-blur-sm focus:border-primary focus:ring-primary outline-none"
                  />
               ))}
            </div>

            {/* Submit Button */}
            <button
               onClick={handleSubmit}
               disabled={isLoading || otp.includes('')}
               className="w-full py-3 px-4 rounded-lg font-semibold text-white transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none bg-gradient-to-r from-primary to-primary/90 hover:shadow-lg hover:shadow-primary/25 cursor-pointer"
            >
               {isLoading ? (
                  <div className="flex items-center justify-center space-x-2">
                     <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                     <span>Verifying...</span>
                  </div>
               ) : (
                  'Verify'
               )}
            </button>
         </div>
      </ParentLayout>
   );
};

export default VerifyOtp;
