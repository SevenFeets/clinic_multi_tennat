/**
 * Statistics Service
 * 
 * Handles all API calls related to dashboard statistics
 */

import { get } from './api';

/**
 * Get dashboard statistics
 * Fetches all dashboard stats in one request
 * 
 * @returns {Promise<Object>} Dashboard stats object
 * @throws {Error} If request fails
 */
export const getDashboardStats = async () => {
  try {
    const data = await get('/stats/dashboard');
    return data;
  } catch (error) {
    console.error('Error fetching dashboard stats:', error);
    throw error;
  }
};

/**
 * Example response format:
 * {
 *   total_patients: 124,
 *   patients_this_month: 12,
 *   today_appointments: 8,
 *   today_completed: 3,
 *   pending_appointments: 15,
 *   revenue_this_month: 12450.00
 * }
 */

