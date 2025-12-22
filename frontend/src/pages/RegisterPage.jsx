import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register as registerUser } from '../services/authService';
import '../styles/RegisterPage.css';

/**
 * RegisterPage Component
 * 
 * Allows new users to create an account for the veterinary clinic.
 * After successful registration, redirects to login page.
 */

function RegisterPage() {
  const navigate = useNavigate();

  // Form state
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    tenant_id: 1, // Default to tenant 1 (cityclinic) for now
  });

  // UI state
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Handle input changes
   */
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error when user starts typing
    setError('');
  };

  /**
   * Validate form before submission
   */
  const validateForm = () => {
    if (!formData.email || !formData.password || !formData.full_name || !formData.confirmPassword) {
      setError('All fields are required');
      return false;
    }

    if (!formData.email.includes('@')) {
      setError('Please enter a valid email address');
      return false;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return false;
    }

    // Password strength requirements (must match backend)
    if (!/\d/.test(formData.password)) {
      setError('Password must contain at least one number');
      return false;
    }

    if (!/[A-Z]/.test(formData.password)) {
      setError('Password must contain at least one uppercase letter');
      return false;
    }

    if (!/[a-z]/.test(formData.password)) {
      setError('Password must contain at least one lowercase letter');
      return false;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    return true;
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Remove confirmPassword before sending to API
      const { confirmPassword, ...registrationData } = formData;

      // Call register API
      await registerUser(registrationData);

      // Success! Redirect to login page
      alert('Account created successfully! Please log in.');
      navigate('/login');
      
    } catch (err) {
      // Handle error
      console.error('Registration error:', err);
      console.log('Error type:', typeof err);
      console.log('Error object:', err);
      
      // Extract error message - ALWAYS convert to string
      let errorMessage = 'Registration failed. Please try again.';
      
      if (typeof err === 'string') {
        errorMessage = err;
      } else if (err instanceof Error && err.message) {
        errorMessage = err.message;
      } else if (err?.message && typeof err.message === 'string') {
        errorMessage = err.message;
      } else if (err?.detail && typeof err.detail === 'string') {
        errorMessage = err.detail;
      } else if (err?.error && typeof err.error === 'string') {
        errorMessage = err.error;
      }
      
      // Ensure it's DEFINITELY a string
      errorMessage = String(errorMessage);
      
      console.log('Final error message (string):', errorMessage);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-card">
          {/* Logo/Header */}
          <div className="register-header">
            <h1>🐾 Veterinary Clinic</h1>
            <h2>Create Your Account</h2>
            <p>Join us to manage your clinic efficiently</p>
          </div>

          {/* Registration Form */}
          <form onSubmit={handleSubmit} className="register-form">
            {/* Error Message */}
            {error && (
              <div className="error-message">
                ⚠️ {String(error)}
              </div>
            )}

            {/* Full Name Input */}
            <div className="form-group">
              <label htmlFor="full_name">Full Name</label>
              <input
                type="text"
                id="full_name"
                name="full_name"
                placeholder="Dr. John Smith"
                value={formData.full_name}
                onChange={handleChange}
                disabled={isLoading}
                required
              />
            </div>

            {/* Email Input */}
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                placeholder="doctor@clinic.com"
                value={formData.email}
                onChange={handleChange}
                disabled={isLoading}
                required
              />
            </div>

            {/* Password Input */}
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                placeholder="Create a strong password"
                value={formData.password}
                onChange={handleChange}
                disabled={isLoading}
                required
              />
              <div className="password-requirements">
                <small>Password must contain:</small>
                <ul>
                  <li>At least 8 characters</li>
                  <li>One uppercase letter (A-Z)</li>
                  <li>One lowercase letter (a-z)</li>
                  <li>One number (0-9)</li>
                </ul>
              </div>
            </div>

            {/* Confirm Password Input */}
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                placeholder="Re-enter your password"
                value={formData.confirmPassword}
                onChange={handleChange}
                disabled={isLoading}
                required
              />
            </div>

            {/* Submit Button */}
            <button 
              type="submit" 
              className="register-button"
              disabled={isLoading}
            >
              {isLoading ? 'Creating Account...' : 'Create Account'}
            </button>

            {/* Login Link */}
            <div className="login-link">
              Already have an account?{' '}
              <Link to="/login">Log in here</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;

