/**
 * Appointment Service
 * Handles all appointment-related API calls
 */

import { get, post, put, del, patch } from './api';
import { ENDPOINTS } from '../utils/constants';

export const getAppointments = async () => {
  
  try {
    const appointments = await get(ENDPOINTS.APPOINTMENTS.LIST);
    return appointments;
  } catch (error) {
    console.error('Error fetching appointments:', error);
    throw error;
  }
};


/**
 * Get single appointment by ID
 * @param {string} id - Appointment ID
 * @returns {Promise<object>}
 */
export const getAppointment = async (id) => {
  try {
    const appointment = await get(ENDPOINTS.APPOINTMENTS.DETAIL(id));
    return appointment;
  } catch (error) {
    console.error('Error fetching appointment:', error);
    throw error;
  }
};

/**
 * Create new appointment
 * @param {object} appointmentData - Appointment data
 * @returns {Promise<object>}
 */
export const createAppointment = async (appointmentData) => {
  try {
    const appointment = await post(ENDPOINTS.APPOINTMENTS.CREATE, appointmentData);
    return appointment;
  } catch (error) {
    console.error('Error creating appointment:', error);
    throw error;
  }
};

/**
 * Update appointment
 * @param {string} id - Appointment ID
 * @param {object} appointmentData - Updated appointment data
 * @returns {Promise<object>}
 */
export const updateAppointment = async (id, appointmentData) => {
  try {
    // Backend uses PATCH method for updates (not PUT)
    const appointment = await patch(ENDPOINTS.APPOINTMENTS.UPDATE(id), appointmentData);
    return appointment;
  } catch (error) {
    console.error('Error updating appointment:', error);
    throw error;
  }
};

/**
 * Delete appointment
 * @param {string} id - Appointment ID
 * @returns {Promise<void>}
 */
export const deleteAppointment = async (id) => {
  try {
    await del(ENDPOINTS.APPOINTMENTS.DELETE(id));
  } catch (error) {
    console.error('Error deleting appointment:', error);
    throw error;
  }
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
