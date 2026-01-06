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
 * Get appointment statistics
 * Fetches comprehensive appointment analytics
 * 
 * @returns {Promise<Object>} Appointment stats object
 * @throws {Error} If request fails
 */
export const getAppointmentStats = async () => {
  try {
    const data = await get('/appointments/stats');
    return data;
  } catch (error) {
    console.error('Error fetching appointment stats:', error);
    throw error;
  }
};

/**
 * Example response format for dashboard stats:
 * {
 *   total_patients: 124,
 *   patients_this_month: 12,
 *   today_appointments: 8,
 *   today_completed: 3,
 *   pending_appointments: 15,
 *   revenue_this_month: 12450.00
 * }
 * 
 * Example response format for appointment stats:
 * {
 *   total_appointments: 450,
 *   scheduled_count: 25,
 *   completed_count: 380,
 *   cancelled_count: 30,
 *   no_show_count: 15,
 *   no_show_rate: 3.8,
 *   average_duration_minutes: 30.5,
 *   appointments_this_month: 85,
 *   appointments_this_week: 20,
 *   upcoming_appointments: 25
 * }
 */

