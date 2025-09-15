'use client';

import React, { useState, createContext, useContext, useEffect } from 'react';
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from '@/lib/api/auth';
import api from '@/lib/axios';

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

type AuthContextType = {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean; // 👈 Add loading state
  login: (access: string, refresh: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true); 

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

  const login = (access: string, refresh: string) => {
    setTokens(access, refresh);
    setAccessToken(access);
    api.get<User>('/auth/me').then(res => setUser(res.data));
  };

  const logout = () => {
    clearTokens();
    setAccessToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, accessToken, isLoading, login, logout }}
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