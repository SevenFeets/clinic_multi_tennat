/**
 * Appointment Service
 * Handles all appointment-related API calls
 */

import { get, post, put, del } from './api';
import { ENDPOINTS } from '../utils/constants';

/**
 * Get all appointments
 * @returns {Promise<Array>}
 */
export const getAppointments = async () => {
  // TODO: Implement get all appointments
  // Hint: GET to ENDPOINTS.APPOINTMENTS.LIST
  
  throw new Error('getAppointments not implemented - your turn!');
};

/**
 * Get single appointment by ID
 * @param {string} id - Appointment ID
 * @returns {Promise<object>}
 */
export const getAppointment = async (id) => {
  // TODO: Implement get appointment by ID
  
  throw new Error('getAppointment not implemented - your turn!');
};

/**
 * Create new appointment
 * @param {object} appointmentData - Appointment data
 * @returns {Promise<object>}
 */
export const createAppointment = async (appointmentData) => {
  // TODO: Implement create appointment
  
  throw new Error('createAppointment not implemented - your turn!');
};

/**
 * Update appointment
 * @param {string} id - Appointment ID
 * @param {object} appointmentData - Updated appointment data
 * @returns {Promise<object>}
 */
export const updateAppointment = async (id, appointmentData) => {
  // TODO: Implement update appointment
  
  throw new Error('updateAppointment not implemented - your turn!');
};

/**
 * Delete appointment
 * @param {string} id - Appointment ID
 * @returns {Promise<void>}
 */
export const deleteAppointment = async (id) => {
  // TODO: Implement delete appointment
  
  throw new Error('deleteAppointment not implemented - your turn!');
};


/**
 * Get today's appointments
 * @returns {Promise<Array>}
 */
export const getTodayAppointments = async () => {
  // Get today's date in YYYY-MM-DD format
  const today = new Date().toISOString().split('T')[0];
  
  // Call API with date filter (API supports date_from and date_to query params)
  // This is more efficient than fetching all appointments
  const appointments = await get(ENDPOINTS.APPOINTMENTS.LIST + `?date_from=${today}&date_to=${today}`);
  
  return appointments;
};
