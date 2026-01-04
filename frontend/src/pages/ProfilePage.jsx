import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getProfile, updateProfile, changePassword } from '../services/profileService';
import '../styles/ProfilePage.css';

/**
 * ProfilePage Component
 * 
 * Allows users to:
 * - Update their name (full_name)
 * - Update their email address
 * - Update their profile photo (photo_url)
 * - Change their password
 */

function ProfilePage() {
    const { user, login } = useAuth();
    const navigate = useNavigate();

    // Profile form state
    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [photoUrl, setPhotoUrl] = useState('');
    
    // Password form state
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    // UI state
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [isChangingPassword, setIsChangingPassword] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    // Fetch current profile on mount
    useEffect(() => {
        fetchProfile();
    }, []);

    /**
     * Fetch current user profile
     */
    const fetchProfile = async () => {
        try {
            setIsLoading(true);
            setError(null);
            const profile = await getProfile();
            setFullName(profile.full_name || '');
            setEmail(profile.email || '');
            setPhotoUrl(profile.photo_url || '');
        } catch (err) {
            console.error('Error fetching profile:', err);
            setError(err.message || 'Failed to load profile');
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Handle profile update (name, email, photo)
     */
    const handleProfileUpdate = async (e) => {
        e.preventDefault();
        
        try {
            setIsSaving(true);
            setError(null);
            setSuccess(null);

            // Build update object with only changed fields
            const updateData = {};
            if (fullName !== user?.full_name) updateData.full_name = fullName;
            if (email !== user?.email) updateData.email = email;
            if (photoUrl !== (user?.photo_url || '')) updateData.photo_url = photoUrl || null;

            // Only send request if there are changes
            if (Object.keys(updateData).length === 0) {
                setSuccess('No changes to save');
                return;
            }

            const updatedUser = await updateProfile(updateData);
            
            // Update auth context with new user data
            // This refreshes the user object across the app
            login({
                user: updatedUser,
                token: localStorage.getItem('token') // Keep existing token
            });

            setSuccess('Profile updated successfully!');
            
            // Clear success message after 3 seconds
            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            console.error('Error updating profile:', err);
            setError(err.message || 'Failed to update profile');
        } finally {
            setIsSaving(false);
        }
    };

    /**
     * Handle password change
     */
    const handlePasswordChange = async (e) => {
        e.preventDefault();
        
        // Validation
        if (newPassword !== confirmPassword) {
            setError('New passwords do not match');
            return;
        }

        if (newPassword.length < 8) {
            setError('Password must be at least 8 characters');
            return;
        }

        try {
            setIsChangingPassword(true);
            setError(null);
            setSuccess(null);

            await changePassword({
                old_password: oldPassword,
                new_password: newPassword
            });

            setSuccess('Password changed successfully!');
            
            // Clear password fields
            setOldPassword('');
            setNewPassword('');
            setConfirmPassword('');
            
            // Clear success message after 3 seconds
            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            console.error('Error changing password:', err);
            setError(err.message || 'Failed to change password');
        } finally {
            setIsChangingPassword(false);
        }
    };

    if (isLoading) {
        return (
            <div className="profile-page">
                <div className="loading">Loading profile... ⏳</div>
            </div>
        );
    }

    return (
        <div className="profile-page">
            {/* Navigation Bar */}
            <nav className="profile-nav">
                <div className="nav-left">
                    <button onClick={() => navigate('/dashboard')} className="back-button">
                        ← Back to Dashboard
                    </button>
                    <h1>👤 Profile Settings</h1>
                </div>
                <div className="nav-right">
                    <span className="user-info">👤 {user?.email}</span>
                </div>
            </nav>

            <main className="profile-main">
                {/* Error/Success Messages */}
                {error && (
                    <div className="alert alert-error">
                        ❌ {error}
                    </div>
                )}
                {success && (
                    <div className="alert alert-success">
                        ✅ {success}
                    </div>
                )}

                {/* Profile Information Section */}
                <section className="profile-section">
                    <h2>Profile Information</h2>
                    <form onSubmit={handleProfileUpdate} className="profile-form">
                        {/* Profile Photo */}
                        <div className="form-group">
                            <label htmlFor="photoUrl">Profile Photo URL</label>
                            <input
                                type="url"
                                id="photoUrl"
                                value={photoUrl}
                                onChange={(e) => setPhotoUrl(e.target.value)}
                                placeholder="https://example.com/photo.jpg"
                                className="form-input"
                            />
                            <small className="form-hint">
                                Enter a URL to your profile photo. File upload coming soon!
                            </small>
                            {photoUrl && (
                                <div className="photo-preview">
                                    <img src={photoUrl} alt="Profile preview" onError={(e) => {
                                        e.target.style.display = 'none';
                                    }} />
                                </div>
                            )}
                        </div>

                        {/* Full Name */}
                        <div className="form-group">
                            <label htmlFor="fullName">Full Name</label>
                            <input
                                type="text"
                                id="fullName"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                required
                                className="form-input"
                            />
                        </div>

                        {/* Email */}
                        <div className="form-group">
                            <label htmlFor="email">Email Address</label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="form-input"
                            />
                            <small className="form-hint">
                                ⚠️ Email verification will be required once SendGrid is configured
                            </small>
                        </div>

                        {/* Submit Button */}
                        <button 
                            type="submit" 
                            className="btn btn-primary"
                            disabled={isSaving}
                        >
                            {isSaving ? 'Saving...' : 'Save Changes'}
                        </button>
                    </form>
                </section>

                {/* Password Change Section */}
                <section className="profile-section">
                    <h2>Change Password</h2>
                    <form onSubmit={handlePasswordChange} className="profile-form">
                        {/* Old Password */}
                        <div className="form-group">
                            <label htmlFor="oldPassword">Current Password</label>
                            <input
                                type="password"
                                id="oldPassword"
                                value={oldPassword}
                                onChange={(e) => setOldPassword(e.target.value)}
                                required
                                className="form-input"
                            />
                        </div>

                        {/* New Password */}
                        <div className="form-group">
                            <label htmlFor="newPassword">New Password</label>
                            <input
                                type="password"
                                id="newPassword"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                required
                                minLength={8}
                                className="form-input"
                            />
                            <small className="form-hint">
                                Must be at least 8 characters with uppercase, lowercase, and number
                            </small>
                        </div>

                        {/* Confirm Password */}
                        <div className="form-group">
                            <label htmlFor="confirmPassword">Confirm New Password</label>
                            <input
                                type="password"
                                id="confirmPassword"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                minLength={8}
                                className="form-input"
                            />
                        </div>

                        {/* Submit Button */}
                        <button 
                            type="submit" 
                            className="btn btn-primary"
                            disabled={isChangingPassword}
                        >
                            {isChangingPassword ? 'Changing...' : 'Change Password'}
                        </button>
                    </form>
                </section>
            </main>
        </div>
    );
}

export default ProfilePage;

