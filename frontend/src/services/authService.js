/**
 * Authentication Service
 * Handles all auth-related API calls
 */

import { post, get } from './api';
import { ENDPOINTS } from '../utils/constants';
import { saveToken, saveUser, removeToken, removeUser } from '../utils/storage';

/**
 * Login user
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{user, token}>}
 */
export const login = async (email, password) => {
  // TODO: Implement login API call
  // Hint: POST to ENDPOINTS.AUTH.LOGIN with email and password
  // FastAPI expects form data for OAuth2, so you might need to adjust
  // Save token and user data after successful login
  
  throw new Error('Login not implemented yet - implement this!');
};

/**
 * Register new user
 * @param {object} userData - User registration data
 * @returns {Promise<object>} User object
 */
export const register = async (userData) => {
  try {
    const response = await post('/auth/register', userData);
    return response;
  } catch (error) {
    throw error;
  }
};

/**
 * Logout user
 */
export const logout = () => {
  // TODO: Clear stored token and user data
  // Hint: Use removeToken() and removeUser() from storage utils
  
  console.log('Logout called - clear your tokens here!');
};

/**
 * Get current user profile
 * @returns {Promise<object>}
 */
export const getCurrentUser = async () => {
  // TODO: Implement get current user
  // Hint: GET to ENDPOINTS.AUTH.ME
  // This requires the token to be in the header (api.js handles this)
  
  throw new Error('getCurrentUser not implemented yet - implement this!');
};

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  // TODO: Check if token exists in storage
  // Hint: Use getToken() from storage utils
  
  return false; // Change this!
};

