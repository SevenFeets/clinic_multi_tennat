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
// Note: Token is stored as plain string, not JSON
export const saveToken = (token) => {
  try {
    localStorage.setItem(STORAGE_KEYS.TOKEN, token);
  } catch (error) {
    console.error('Error saving token:', error);
  }
};

export const getToken = () => {
  try {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
  } catch (error) {
    console.error('Error getting token:', error);
    return null;
  }
};

export const removeToken = () => removeItem(STORAGE_KEYS.TOKEN);

export const saveUser = (user) => setItem(STORAGE_KEYS.USER, user);
export const getUser = () => getItem(STORAGE_KEYS.USER);
export const removeUser = () => removeItem(STORAGE_KEYS.USER);

// Note: Tenant is stored as plain string, not JSON
export const saveTenant = (tenant) => {
  try {
    localStorage.setItem(STORAGE_KEYS.TENANT, tenant);
  } catch (error) {
    console.error('Error saving tenant:', error);
  }
};

export const getTenant = () => {
  try {
    return localStorage.getItem(STORAGE_KEYS.TENANT);
  } catch (error) {
    console.error('Error getting tenant:', error);
    return null;
  }
};

export const removeTenant = () => removeItem(STORAGE_KEYS.TENANT);

