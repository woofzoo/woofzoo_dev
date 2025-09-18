'use client';

import React, { useState, createContext, useContext, useEffect } from 'react';
import { clearTokens, getAccessToken, setTokens, login as apiLogin } from '@/lib/api/auth';
import api from '@/lib/axios';
import { useToast } from '@/components/toast/ToastProvider';

type User = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  roles: string[];
  is_active: boolean;
  is_verified: boolean;
  personalization: {
    language: string;
    theme: string;
  };
  created_at: string;
  updated_at: string;
  last_login: string;
};

type LoginCredentials = {
  email: string;
  password: string;
};

type AuthContextType = {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean;
  isLoggingIn: boolean;
  loginError: string | null;
  signIn: (credentials: LoginCredentials) => Promise<User | null>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const { showSuccess, showError, showInfo, showWarning } = useToast();
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  useEffect(() => {
    const initializeAuth = async () => {
      const storedAccessToken = getAccessToken();
      if (storedAccessToken) {
        setAccessToken(storedAccessToken);
        try {
          const res = await api.get<User>('/auth/me');
          setUser(res.data);
        } catch (err) {
          console.error('Failed to authenticate with stored token:', err);
          logout();
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const signIn = async ({ email, password }: LoginCredentials): Promise<User | null> => {
    setIsLoggingIn(true);
    setLoginError(null);
    try {
      const data = await apiLogin({ email, password });

      if (data && data?.tokens) {
        setTokens(data.tokens.access_token, data.tokens.refresh_token);
        setAccessToken(data.tokens.access_token);

        const userProfile = await api.get<User>('/auth/me');
        setUser(userProfile.data);
        setIsLoggingIn(false);
        // Don't show success toast here because navigation happens immediately after login.
        // The dashboard page will read a query param and show the success toast after navigation.

        return userProfile.data;
      } else {
        throw new Error('Login failed: No authentication token received.');
      }
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || 'Invalid credentials. Please try again.';
      setLoginError(errorMessage);
      setIsLoggingIn(false);
      showError("Login Failed", errorMessage, 5000);
      return null;
    }
  };

  const logout = () => {
    clearTokens();
    setAccessToken(null);
    setUser(null);
    showSuccess(
      'Logged Out Successfully !',
      'You have been logged out successfully.',
      5000
    );
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        isLoading,
        isLoggingIn,
        loginError,
        signIn,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};