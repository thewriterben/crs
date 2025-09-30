import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '@/lib/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access_token'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refresh_token'));

  // Check if user is authenticated on mount
  useEffect(() => {
    const verifyToken = async () => {
      if (accessToken) {
        try {
          const response = await authApi.verifyToken(accessToken);
          if (response.valid) {
            setUser(response.user);
          } else {
            // Try to refresh token
            await refreshAccessToken();
          }
        } catch (error) {
          console.error('Token verification failed:', error);
          // Try to refresh token
          await refreshAccessToken();
        }
      }
      setLoading(false);
    };

    verifyToken();
  }, []);

  const refreshAccessToken = async () => {
    if (!refreshToken) {
      logout();
      return;
    }

    try {
      const response = await authApi.refreshToken(refreshToken);
      if (response.access_token) {
        setAccessToken(response.access_token);
        localStorage.setItem('access_token', response.access_token);
        // Verify the new token
        const verifyResponse = await authApi.verifyToken(response.access_token);
        if (verifyResponse.valid) {
          setUser(verifyResponse.user);
        }
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
    }
  };

  const login = async (username, password, mfaCode = null) => {
    try {
      const response = await authApi.login(username, password, mfaCode);
      
      if (response.mfa_required) {
        return { success: false, mfaRequired: true };
      }

      if (response.access_token && response.refresh_token) {
        setAccessToken(response.access_token);
        setRefreshToken(response.refresh_token);
        setUser(response.user);
        
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);
        
        return { success: true, user: response.user };
      }

      throw new Error('Invalid response from server');
    } catch (error) {
      console.error('Login failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || error.message || 'Login failed'
      };
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await authApi.register(username, email, password);
      
      if (response.user) {
        // Auto-login after registration
        const loginResult = await login(username, password);
        return loginResult;
      }

      throw new Error('Invalid response from server');
    } catch (error) {
      console.error('Registration failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || error.message || 'Registration failed'
      };
    }
  };

  const logout = async () => {
    try {
      if (accessToken) {
        await authApi.logout(accessToken);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setAccessToken(null);
      setRefreshToken(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  };

  const updateProfile = async (data) => {
    try {
      const response = await authApi.updateProfile(accessToken, data);
      if (response.user) {
        setUser(response.user);
        return { success: true, user: response.user };
      }
      throw new Error('Invalid response from server');
    } catch (error) {
      console.error('Profile update failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || error.message || 'Profile update failed'
      };
    }
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      await authApi.changePassword(accessToken, currentPassword, newPassword);
      return { success: true };
    } catch (error) {
      console.error('Password change failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || error.message || 'Password change failed'
      };
    }
  };

  const enableMFA = async () => {
    try {
      const response = await authApi.enableMFA(accessToken);
      if (response.secret) {
        // Update user object
        const updatedUser = { ...user, mfa_enabled: true };
        setUser(updatedUser);
        return { success: true, secret: response.secret };
      }
      throw new Error('Invalid response from server');
    } catch (error) {
      console.error('MFA enable failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || error.message || 'Failed to enable MFA'
      };
    }
  };

  const disableMFA = async (password) => {
    try {
      await authApi.disableMFA(accessToken, password);
      // Update user object
      const updatedUser = { ...user, mfa_enabled: false };
      setUser(updatedUser);
      return { success: true };
    } catch (error) {
      console.error('MFA disable failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || error.message || 'Failed to disable MFA'
      };
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    accessToken,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    enableMFA,
    disableMFA,
    refreshAccessToken
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
