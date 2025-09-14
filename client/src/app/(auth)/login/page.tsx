'use client'

import ParentLayout from '@/components/layout/ParentLayout';
import Input from '@/components/ui/Input';
import { login, setTokens } from '@/lib/api/auth';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';

const LoginPage = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const data = await login({ email, password });

      if (data && data?.tokens) {
        setTokens(data.tokens.access_token, data.tokens.refresh_token);
        router.push('/dashboard/434');
      } else {
        setError('Login failed: No authentication token received.');
      }
    } catch (err: any) {
      console.error('Login error:', err);
      const errorMessage =
        err.response?.data?.message || 'Invalid credentials. Please try again later';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }

    await new Promise(resolve => setTimeout(resolve, 1500));
    console.log('Login attempt:', { email, password, rememberMe });
  };

  return (
    <ParentLayout className="">
      <div className="space-y-6">
        {/* Logo + Heading */}
        <div className="text-center space-y-5">
          <div className="w-[10rem] rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <img src="/group-1.svg" alt="TM Logo" className="object-contain" />
          </div>
          <div className="space-y-2">
            <h1 className="text-xl font-bold text-gray-900 tracking-tight">
              Welcome Back
            </h1>
            <p className="text-gray-600">Sign in to your account to continue</p>
          </div>
        </div>

        {/* ✅ Login Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            buttonType="email"
            label="Email Address"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full border-gray-200/80 bg-accent-pastel/40 p-2 backdrop-blur-sm focus:border-primary focus:ring-primary/20 placeholder:text-gray-400 outline-none"
          />

          <Input
            buttonType="password"
            label="Password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full border-gray-200/80 bg-accent-pastel/40 p-2 backdrop-blur-sm focus:border-primary focus:ring-primary/20 placeholder:text-gray-400 outline-none"
          />

          {/* Remember Me & Forgot Password */}
          <div className="flex items-center justify-between">
            <label className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary/20 focus:ring-2"
                style={{ accentColor: 'var(--primary-color)' }}
              />
              <span className="text-sm text-gray-700 group-hover:text-gray-900 transition-colors">
                Remember me
              </span>
            </label>
            <button
              type="button"
              className="text-sm font-medium text-secondary hover:text-secondary/80 hover:underline transition-all duration-200 cursor-pointer"
              onClick={() => router.push('/forgot-password')}
            >
              Forgot password?
            </button>
          </div>

          {/* ✅ Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 rounded-lg font-semibold text-white transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none bg-gradient-to-r from-primary to-primary/90 hover:shadow-lg hover:shadow-primary/25 cursor-pointer"
          >
            {isLoading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Signing you in...</span>
              </div>
            ) : (
              'Sign In'
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
    </ParentLayout>
  );
};

export default LoginPage;
