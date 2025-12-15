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
  // TODO: Implement get all patients
  // Hint: GET to ENDPOINTS.PATIENTS.LIST
  
  throw new Error('getPatients not implemented - your turn!');
};

/**
 * Get single patient by ID
 * @param {string} id - Patient ID
 * @returns {Promise<object>}
 */
export const getPatient = async (id) => {
  // TODO: Implement get patient by ID
  // Hint: GET to ENDPOINTS.PATIENTS.DETAIL(id)
  
  throw new Error('getPatient not implemented - your turn!');
};

/**
 * Create new patient
 * @param {object} patientData - Patient data
 * @returns {Promise<object>}
 */
export const createPatient = async (patientData) => {
  // TODO: Implement create patient
  // Hint: POST to ENDPOINTS.PATIENTS.CREATE with patientData
  
  throw new Error('createPatient not implemented - your turn!');
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

