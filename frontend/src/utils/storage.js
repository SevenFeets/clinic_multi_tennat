/**
 * Local Storage Helper Functions
 * Provides safe and typed access to localStorage
 */

import { STORAGE_KEYS } from './constants';

/**
 * Save data to localStorage
 * @param {string} key - Storage key
 * @param {any} value - Value to store (will be JSON stringified)
 */
export const setItem = (key, value) => {
  try {
    const serialized = JSON.stringify(value);
    localStorage.setItem(key, serialized);
  } catch (error) {
    console.error('Error saving to localStorage:', error);
  }
};

/**
 * Get data from localStorage
 * @param {string} key - Storage key
 * @returns {any} Parsed value or null
 */
export const getItem = (key) => {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (error) {
    console.error('Error reading from localStorage:', error);
    return null;
  }
};

/**
 * Remove item from localStorage
 * @param {string} key - Storage key
 */
export const removeItem = (key) => {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error('Error removing from localStorage:', error);
  }
};

/**
 * Clear all items from localStorage
 */
export const clearAll = () => {
  try {
    localStorage.clear();
  } catch (error) {
    console.error('Error clearing localStorage:', error);
  }
};

// Auth-specific helpers
export const saveToken = (token) => setItem(STORAGE_KEYS.TOKEN, token);
export const getToken = () => getItem(STORAGE_KEYS.TOKEN);
export const removeToken = () => removeItem(STORAGE_KEYS.TOKEN);

export const saveUser = (user) => setItem(STORAGE_KEYS.USER, user);
export const getUser = () => getItem(STORAGE_KEYS.USER);
export const removeUser = () => removeItem(STORAGE_KEYS.USER);

export const saveTenant = (tenant) => setItem(STORAGE_KEYS.TENANT, tenant);
export const getTenant = () => getItem(STORAGE_KEYS.TENANT);
export const removeTenant = () => removeItem(STORAGE_KEYS.TENANT);

