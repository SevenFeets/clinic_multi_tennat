/**
 * Base API Client
 * Handles all HTTP requests to the backend
 */

import { API_URL, DEFAULT_TENANT } from '../utils/constants';
import { getToken, getTenant } from '../utils/storage';

/**
 * Base fetch wrapper with authentication and error handling
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise<any>}
 */
export const apiClient = async (endpoint, options = {}) => {
  const token = getToken();
  const tenant = getTenant() || DEFAULT_TENANT; // Use default tenant if none stored
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      'X-Tenant-ID': tenant, // Always include tenant header
      ...options.headers,
    },
  };

  try {
    const response = await fetch(`${API_URL}${endpoint}`, config);
    
    // Handle non-JSON responses (like 204 No Content)
    if (response.status === 204) {
      return null;
    }

    // Try to parse JSON response
    let data;
    try {
      data = await response.json();
    } catch (parseError) {
      console.error('Failed to parse JSON response:', parseError);
      throw new Error('Invalid response from server. Please try again.');
    }

    // Check if request failed
    if (!response.ok) {
      // Extract error message from various possible formats
      const errorMessage = 
        data.detail || 
        data.message || 
        data.error ||
        (typeof data === 'string' ? data : null) ||
        `Request failed with status ${response.status}`;
      
      throw new Error(errorMessage);
    }

    return data;
  } catch (error) {
    console.error('API Error:', error);
    
    // If error is already an Error object with a message, throw it
    if (error instanceof Error && error.message) {
      throw error;
    }
    
    // Otherwise, create a new Error with a proper message
    throw new Error('Network error. Please check your connection and try again.');
  }
};

/**
 * GET request
 */
export const get = (endpoint) => apiClient(endpoint, { method: 'GET' });

/**
 * POST request
 */
export const post = (endpoint, data) =>
  apiClient(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });

/**
 * PUT request
 */
export const put = (endpoint, data) =>
  apiClient(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  });

/**
 * DELETE request
 */
export const del = (endpoint) => apiClient(endpoint, { method: 'DELETE' });

/**
 * PATCH request
 */
export const patch = (endpoint, data) =>
  apiClient(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });

