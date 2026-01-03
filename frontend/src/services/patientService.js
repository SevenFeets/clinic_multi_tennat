/**
 * Patient Service
 * Handles all patient-related API calls
 */

import { get, post, put, del } from './api';
import { ENDPOINTS } from '../utils/constants';

/**
 * Get all patients
 * @returns {Promise<Array>}
 */
export const getPatients = async () => {
  try {
    const data = await get('/patients');
    return data;
  } catch (error) {
    console.error('Error fetching patients:', error);
    throw error;
  }
};

/**
 * Get single patient by ID
 * @param {string} id - Patient ID
 * @returns {Promise<object>}
 */
export const getPatient = async (id) => {

  try {
    const patient = await get(ENDPOINTS.PATIENTS.DETAIL(id));
    return patient;
  }
  catch (error) {
    console.error('Error fetching patient:', error);
    throw error;
  }
  
};

/**
 * Create new patient
 * @param {object} patientData - Patient data
 * @returns {Promise<object>}
 */
export const createPatient = async (patientData) => {
  try {
    const patient = await post(ENDPOINTS.PATIENTS.CREATE, patientData);
    return patient;
  }
  catch (error) {
    console.error('Error creating patient:', error);
    throw error;
  }
};

/**
 * Update patient
 * @param {string} id - Patient ID
 * @param {object} patientData - Updated patient data
 * @returns {Promise<object>}
 */
export const updatePatient = async (id, patientData) => {
  // TODO: Implement update patient
  // Hint: PUT to ENDPOINTS.PATIENTS.UPDATE(id) with patientData
  
  throw new Error('updatePatient not implemented - your turn!');
};

/**
 * Delete patient
 * @param {string} id - Patient ID
 * @returns {Promise<void>}
 */
export const deletePatient = async (id) => {
  // TODO: Implement delete patient
  // Hint: DELETE to ENDPOINTS.PATIENTS.DELETE(id)
  
  throw new Error('deletePatient not implemented - your turn!');
};

