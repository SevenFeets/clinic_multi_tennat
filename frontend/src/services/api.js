/**
 * Base API Client
 * Handles all HTTP requests to the backend
 */

import { API_URL } from '../utils/constants';
import { getToken, getTenant } from '../utils/storage';

/**
 * Base fetch wrapper with authentication and error handling
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise<any>}
 */
export const apiClient = async (endpoint, options = {}) => {
  const token = getToken();
  const tenant = getTenant();
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...(tenant && { 'X-Tenant-ID': tenant }),
      ...options.headers,
    },
  };

  try {
    const response = await fetch(`${API_URL}${endpoint}`, config);
    
    // Handle non-JSON responses (like 204 No Content)
    if (response.status === 204) {
      return null;
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || data.message || 'Something went wrong');
    }

    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
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

