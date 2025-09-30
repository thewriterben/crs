import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';
import { User, Mail, Lock, Shield, Loader2, Check, X } from 'lucide-react';

export default function UserProfile() {
  const { user, updateProfile, changePassword, enableMFA, disableMFA, logout } = useAuth();
  
  // Profile update state
  const [email, setEmail] = useState(user?.email || '');
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileError, setProfileError] = useState('');
  const [profileSuccess, setProfileSuccess] = useState('');

  // Password change state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordError, setPasswordError] = useState('');
  const [passwordSuccess, setPasswordSuccess] = useState('');

  // MFA state
  const [mfaSecret, setMfaSecret] = useState('');
  const [mfaPassword, setMfaPassword] = useState('');
  const [mfaLoading, setMfaLoading] = useState(false);
  const [mfaError, setMfaError] = useState('');
  const [mfaSuccess, setMfaSuccess] = useState('');

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setProfileError('');
    setProfileSuccess('');
    setProfileLoading(true);

    try {
      const result = await updateProfile({ email });
      if (result.success) {
        setProfileSuccess('Profile updated successfully');
      } else {
        setProfileError(result.error || 'Failed to update profile');
      }
    } catch (err) {
      setProfileError('An error occurred while updating profile');
    } finally {
      setProfileLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setPasswordError('');
    setPasswordSuccess('');

    if (newPassword !== confirmNewPassword) {
      setPasswordError('New passwords do not match');
      return;
    }

    setPasswordLoading(true);

    try {
      const result = await changePassword(currentPassword, newPassword);
      if (result.success) {
        setPasswordSuccess('Password changed successfully. You will be logged out.');
        setCurrentPassword('');
        setNewPassword('');
        setConfirmNewPassword('');
        // Logout after 2 seconds
        setTimeout(() => logout(), 2000);
      } else {
        setPasswordError(result.error || 'Failed to change password');
      }
    } catch (err) {
      setPasswordError('An error occurred while changing password');
    } finally {
      setPasswordLoading(false);
    }
  };

  const handleEnableMFA = async () => {
    setMfaError('');
    setMfaSuccess('');
    setMfaLoading(true);

    try {
      const result = await enableMFA();
      if (result.success) {
        setMfaSecret(result.secret);
        setMfaSuccess('MFA enabled successfully. Save this secret: ' + result.secret);
      } else {
        setMfaError(result.error || 'Failed to enable MFA');
      }
    } catch (err) {
      setMfaError('An error occurred while enabling MFA');
    } finally {
      setMfaLoading(false);
    }
  };

  const handleDisableMFA = async (e) => {
    e.preventDefault();
    setMfaError('');
    setMfaSuccess('');
    setMfaLoading(true);

    try {
      const result = await disableMFA(mfaPassword);
      if (result.success) {
        setMfaSuccess('MFA disabled successfully');
        setMfaPassword('');
        setMfaSecret('');
      } else {
        setMfaError(result.error || 'Failed to disable MFA');
      }
    } catch (err) {
      setMfaError('An error occurred while disabling MFA');
    } finally {
      setMfaLoading(false);
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* User Info */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <User className="w-5 h-5" />
            Profile Information
          </CardTitle>
          <CardDescription className="text-gray-400">
            View and update your profile information
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-400">Username</p>
              <p className="text-white font-medium">{user.username}</p>
            </div>
            <div>
              <p className="text-gray-400">Member Since</p>
              <p className="text-white font-medium">
                {new Date(user.created_at).toLocaleDateString()}
              </p>
            </div>
            <div>
              <p className="text-gray-400">Last Login</p>
              <p className="text-white font-medium">
                {user.last_login ? new Date(user.last_login).toLocaleDateString() : 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-gray-400">Account Status</p>
              <p className="text-white font-medium">
                {user.is_active ? (
                  <span className="text-green-400">Active</span>
                ) : (
                  <span className="text-red-400">Inactive</span>
                )}
              </p>
            </div>
          </div>

          <Separator className="bg-gray-700" />

          <form onSubmit={handleProfileUpdate} className="space-y-4">
            {profileError && (
              <Alert variant="destructive">
                <AlertDescription>{profileError}</AlertDescription>
              </Alert>
            )}
            {profileSuccess && (
              <Alert className="border-green-500 bg-green-500/10">
                <Check className="h-4 w-4 text-green-500" />
                <AlertDescription className="text-green-500">{profileSuccess}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="email" className="text-white flex items-center gap-2">
                <Mail className="w-4 h-4" />
                Email
              </Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={profileLoading}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>

            <Button type="submit" disabled={profileLoading}>
              {profileLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Updating...
                </>
              ) : (
                'Update Profile'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Change Password */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Lock className="w-5 h-5" />
            Change Password
          </CardTitle>
          <CardDescription className="text-gray-400">
            Update your password to keep your account secure
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handlePasswordChange} className="space-y-4">
            {passwordError && (
              <Alert variant="destructive">
                <AlertDescription>{passwordError}</AlertDescription>
              </Alert>
            )}
            {passwordSuccess && (
              <Alert className="border-green-500 bg-green-500/10">
                <Check className="h-4 w-4 text-green-500" />
                <AlertDescription className="text-green-500">{passwordSuccess}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="currentPassword" className="text-white">Current Password</Label>
              <Input
                id="currentPassword"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
                disabled={passwordLoading}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="newPassword" className="text-white">New Password</Label>
              <Input
                id="newPassword"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                disabled={passwordLoading}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmNewPassword" className="text-white">Confirm New Password</Label>
              <Input
                id="confirmNewPassword"
                type="password"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                required
                disabled={passwordLoading}
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>

            <Button type="submit" disabled={passwordLoading}>
              {passwordLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Changing...
                </>
              ) : (
                'Change Password'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Multi-Factor Authentication */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Multi-Factor Authentication
          </CardTitle>
          <CardDescription className="text-gray-400">
            Add an extra layer of security to your account
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {mfaError && (
            <Alert variant="destructive">
              <AlertDescription>{mfaError}</AlertDescription>
            </Alert>
          )}
          {mfaSuccess && (
            <Alert className="border-green-500 bg-green-500/10">
              <Check className="h-4 w-4 text-green-500" />
              <AlertDescription className="text-green-500">{mfaSuccess}</AlertDescription>
            </Alert>
          )}

          <div className="flex items-center justify-between p-4 bg-gray-700/50 rounded-lg">
            <div>
              <p className="text-white font-medium">MFA Status</p>
              <p className="text-sm text-gray-400">
                {user.mfa_enabled ? 'Enabled' : 'Disabled'}
              </p>
            </div>
            <div>
              {user.mfa_enabled ? (
                <span className="text-green-400 flex items-center gap-2">
                  <Check className="w-4 h-4" />
                  Active
                </span>
              ) : (
                <span className="text-gray-400 flex items-center gap-2">
                  <X className="w-4 h-4" />
                  Inactive
                </span>
              )}
            </div>
          </div>

          {!user.mfa_enabled ? (
            <div className="space-y-4">
              <p className="text-sm text-gray-400">
                Enable MFA to add an extra layer of security to your account using an authenticator app.
              </p>
              <Button onClick={handleEnableMFA} disabled={mfaLoading}>
                {mfaLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Enabling...
                  </>
                ) : (
                  'Enable MFA'
                )}
              </Button>
              {mfaSecret && (
                <div className="p-4 bg-gray-700 rounded-lg">
                  <p className="text-sm text-gray-400 mb-2">Save this secret in your authenticator app:</p>
                  <code className="text-white bg-gray-900 px-3 py-2 rounded block break-all">
                    {mfaSecret}
                  </code>
                </div>
              )}
            </div>
          ) : (
            <form onSubmit={handleDisableMFA} className="space-y-4">
              <p className="text-sm text-gray-400">
                To disable MFA, please enter your password for verification.
              </p>
              <div className="space-y-2">
                <Label htmlFor="mfaPassword" className="text-white">Password</Label>
                <Input
                  id="mfaPassword"
                  type="password"
                  value={mfaPassword}
                  onChange={(e) => setMfaPassword(e.target.value)}
                  required
                  disabled={mfaLoading}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              <Button type="submit" variant="destructive" disabled={mfaLoading}>
                {mfaLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Disabling...
                  </>
                ) : (
                  'Disable MFA'
                )}
              </Button>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
