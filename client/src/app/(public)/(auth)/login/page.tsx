'use client';

import ParentLayout from '@/components/layout/ParentLayout';
import { PlayfairDisplay } from '@/components/ui/Fonts/Font';
import Input from '@/components/ui/Input';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';

const LoginPage = () => {
  const router = useRouter();
  const { signIn, isLoggingIn, loginError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await signIn({ email, password });
  };

  return (
    <ParentLayout className="flex min-h-screen">
      <div className='w-1/2 flex items-center justify-center'>
        <img src="brandImage.png" alt="Brand" className="w-[30rem] h-[90vh] object-cover rounded-md shadow-lg" />
      </div>

      {/* Right Side - Login Form (50%) */}
      <div className="w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md space-y-6">
          {/* Logo + Heading */}
          <div className="text-center space-y-5">
            <div className="w-[6rem] rounded-2xl mx-auto mb-4 flex items-center justify-center">
              <img src="/group-1.svg" alt="TM Logo" className="object-contain" />
            </div>
            <div className="space-y-3">
              <h1 className={`text-6xl font-light text-primary ${PlayfairDisplay.className}`}>
                Hello There !
              </h1>
              <p className="text-gray-500 text-md">Please login to your account to continue</p>
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              buttonType="email"
              label="Email ID"
              placeholder="Enter your email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-2 backdrop-blur-sm focus:ring-primary/20 placeholder:text-gray-400 outline-none border-b border-gray-300 rounded-l-md rounded-r-md"
            />

            <Input
              buttonType="password"
              label="Password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-2 backdrop-blur-sm focus:ring-primary/20 placeholder:text-gray-400 outline-none border-b border-gray-300 rounded-l-md rounded-r-md"
            />

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <button
                type="button"
                className="text-sm text-secondary hover:text-secondary/80 hover:underline transition-all duration-200 cursor-pointer italic"
                onClick={() => router.push('/forgot-password')}
              >
                View Terms and Conditions
              </button>
              <button
                type="button"
                className="text-sm text-secondary hover:text-secondary/80 hover:underline transition-all duration-200 cursor-pointer italic"
                onClick={() => router.push('/forgot-password')}
              >
                Forgot password?
              </button>
            </div>

            {/* Display error from context */}
            {loginError && (
              <div className="text-sm text-center text-red-600 bg-red-100 p-2 rounded-md">
                {loginError}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoggingIn}
              className={`${PlayfairDisplay.className} tracking-wide w-full py-3 px-4 rounded-lg font-semibold text-white transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none bg-gradient-to-r from-primary to-primary/90 hover:shadow-lg hover:shadow-primary/25 cursor-pointer`}
            >
              {isLoggingIn ? (
                <div className={`flex items-center justify-center space-x-2`}>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Logging you in...</span>
                </div>
              ) : (
                'Log In'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="relative flex items-center justify-center my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-200/60" />
            </div>
          </div>

          {/* Trust Indicators */}
          <div className="flex items-center justify-center space-x-6 pt-4">
            <div className="flex items-center space-x-1.5 text-xs text-gray-500">
              <svg className="w-4 h-4 text-success" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>SSL Secured</span>
            </div>
          </div>
        </div>
      </div>
    </ParentLayout>
  );
};

export default LoginPage;