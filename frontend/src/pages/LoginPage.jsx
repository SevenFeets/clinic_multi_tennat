import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/LoginPage.css';

/**
 * LoginPage Component
 * 
 * This is the page where users log in to access the clinic system.
 * It includes:
 * - Email and password input fields
 * - Form validation
 * - Error handling
 * - Connection to your Django backend
 */

function LoginPage() {
  // Get auth functions from context
  const { login } = useAuth();
  
  // useNavigate lets us redirect user to other pages
  const navigate = useNavigate();

  // Form state - tracks what user types
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  // UI state - tracks loading and errors
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  /**
   * Handle input changes
   * When user types in email or password, update state
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    setError('');
  };

  /**
   * Handle form submission
   * Sends login request to Django backend
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload
    setError('');
    setIsLoading(true);

    try {
      // Get API URL from environment variables
      const apiUrl = import.meta.env.VITE_API_URL;
      const tenantId = import.meta.env.VITE_DEFAULT_TENANT;

      // Make API request to Django backend
      const response = await fetch(`${apiUrl}/api/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': tenantId, // Multi-tenant header
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Login failed
        throw new Error(data.error || 'Login failed');
      }

      // Login successful! 🎉
      // Save user info to context (which also saves to localStorage)
      login({
        user: data.user,
        token: data.token,
      });

      // Redirect to dashboard
      navigate('/dashboard');

    } catch (err) {
      // Show error message to user
      setError(err.message || 'An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {/* Header */}
        <div className="login-header">
          <h1>🏥 Clinic Management</h1>
          <p>Sign in to your account</p>
        </div>

        {/* Show error message if login fails */}
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="login-form">
          {/* Email Input */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="doctor@clinic.com"
              required
              autoComplete="email"
            />
          </div>

          {/* Password Input */}
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              autoComplete="current-password"
            />
          </div>

          {/* Submit Button */}
          <button 
            type="submit" 
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {/* Footer */}
        <div className="login-footer">
          <p>Don't have an account? Contact your administrator</p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;

