/**
 * Profile Service
 * 
 * Handles all API calls related to user profile management
 */

import { get, patch } from './api';

/**
 * Get current user profile
 * @returns {Promise<Object>} User profile object
 * @throws {Error} If request fails
 */
export const getProfile = async () => {
  try {
    const data = await get('/auth/me');
    return data;
  } catch (error) {
    console.error('Error fetching profile:', error);
    throw error;
  }
};

/**
 * Update user profile (name, email, photo_url)
 * @param {Object} profileData - Profile data to update
 * @param {string} [profileData.full_name] - New full name
 * @param {string} [profileData.email] - New email address
 * @param {string} [profileData.photo_url] - New photo URL
 * @returns {Promise<Object>} Updated user object
 * @throws {Error} If request fails
 */
export const updateProfile = async (profileData) => {
  try {
    const data = await patch('/auth/me', profileData);
    return data;
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
};

/**
 * Change user password
 * @param {Object} passwordData - Password change data
 * @param {string} passwordData.old_password - Current password
 * @param {string} passwordData.new_password - New password
 * @returns {Promise<Object>} Updated user object
 * @throws {Error} If request fails
 */
export const changePassword = async (passwordData) => {
  try {
    const data = await patch('/auth/me/password', passwordData);
    return data;
  } catch (error) {
    console.error('Error changing password:', error);
    throw error;
  }
};

