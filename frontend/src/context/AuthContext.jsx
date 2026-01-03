import { createContext, useState, useContext, useEffect } from 'react';
import { STORAGE_KEYS } from '../utils/constants';

/**
 * AuthContext - Manages user authentication state across the entire app
 * 
 * This context provides:
 * - user: The logged-in user object (or null if not logged in)
 * - token: JWT token for API authentication
 * - login(userData): Function to log a user in
 * - logout(): Function to log a user out
 * - isLoading: Whether we're checking if user is already logged in
 */

// 1. Create the context (like a "data broadcasting station")
const AuthContext = createContext(null);

// 2. Create the Provider component (wraps your app to share auth state)
export function AuthProvider({ children }) {
  // State to hold user information
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // When app loads, check if user was already logged in (from localStorage)
  useEffect(() => {
    checkAuth();
  }, []);

  /**
   * Check if user is already authenticated
   * (runs when app first loads)
   */
  const checkAuth = () => {
    try {
      // Look for saved token in browser storage
      const savedToken = localStorage.getItem(STORAGE_KEYS.TOKEN);
      const savedUser = localStorage.getItem(STORAGE_KEYS.USER);

      if (savedToken && savedUser) {
        // User was logged in before, restore their session
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      }
    } catch (error) {
      console.error('Error checking auth:', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Login function - called when user successfully logs in
   * @param {Object} userData - Object containing user info and token
   */
  const login = (userData) => {
    // Save user data to state
    setUser(userData.user);
    setToken(userData.token);

    // Save to localStorage so user stays logged in after page refresh
    localStorage.setItem(STORAGE_KEYS.TOKEN, userData.token);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData.user));
  };

  /**
   * Register function - called when user signs up
   * @param {Object} userData - Object containing new user info
   */
  const register = (userData) => {
    // After registration, we don't automatically log in
    // User will need to login separately for security
    // Just return success
    return userData;
  };

  /**
   * Logout function - called when user clicks logout
   */
  const logout = () => {
    // Clear state
    setUser(null);
    setToken(null);

    // Clear localStorage
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  };

  // The value that will be accessible to all components
  const value = {
    user,
    token,
    login,
    register,
    logout,
    isLoading,
    isAuthenticated: !!user, // true if user exists, false otherwise
  };

  // Provide the auth state to all child components
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// 3. Custom hook to use auth context easily
// Usage: const { user, login, logout } = useAuth();
export function useAuth() {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  
  return context;
}

