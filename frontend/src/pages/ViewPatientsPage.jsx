import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getPatients } from '../services/patientService';
import '../styles/ViewPatientsPage.css';

/**
 * ViewPatientsPage Component
 * 
 * This page displays a list of all patients (pets) in the clinic.
 * 
 * React Concepts Used:
 * - useState: To store data that can change (patients list, loading state, errors)
 * - useEffect: To fetch data when the page loads
 * - Conditional Rendering: Show different content based on state
 */

function ViewPatientsPage() {

  // 1. HOOKS - These manage the component's state and side effects
  // Get the current logged-in user info
  const { user } = useAuth();
  
  // useNavigate allows us to redirect to other pages
  const navigate = useNavigate();

  // useState creates a piece of state (data that can change)
  // Format: const [value, setValue] = useState(initialValue)
  
  // Store the list of patients
  const [patients, setPatients] = useState([]);
  
  // Track if we're currently loading data
  const [isLoading, setIsLoading] = useState(true);
  
  // Store any error messages
  const [error, setError] = useState(null);
  
  // Store search query for filtering patients
  const [searchQuery, setSearchQuery] = useState('');

  // ==========================================
  // 2. FETCH DATA - Load patients when page loads
  // ==========================================
  
  // useEffect runs code when the component mounts (appears on screen)
  // The empty [] means "run once when page loads"
  useEffect(() => {
    fetchPatients();
  }, []); // Empty array = run once on mount

  /**
   * Fetch patients from the backend
   */
  const fetchPatients = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Call the API to get patients
      const data = await getPatients();
      
      // Update state with the fetched data
      setPatients(data);
    } catch (err) {
      console.error('Error loading patients:', err);
      setError(err.message || 'Failed to load patients');
    } finally {
      // This runs whether success or error
      setIsLoading(false);
    }
  };

  // ==========================================
  // 3. HELPER FUNCTIONS
  // ==========================================
  
  /**
   * Filter patients based on search query
   */
  const filteredPatients = patients.filter(patient => {
    if (!searchQuery) return true; // Show all if no search
    
    const query = searchQuery.toLowerCase();
    return (
      patient.pet_name?.toLowerCase().includes(query) ||
      patient.owner_first_name?.toLowerCase().includes(query) ||
      patient.owner_last_name?.toLowerCase().includes(query) ||
      patient.species?.toLowerCase().includes(query) ||
      patient.breed?.toLowerCase().includes(query)
    );
  });

  /**
   * Calculate pet's age from date of birth
   */
  const calculateAge = (dateOfBirth) => {
    if (!dateOfBirth) return 'Unknown';
    
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    
    return age > 0 ? `${age} years` : 'Less than 1 year';
  };

  /**
   * Navigate to patient details page
   */
  const handleViewPatient = (patientId) => {
    navigate(`/patients/${patientId}`);
  };

  // ==========================================
  // 4. RENDER - What shows on the screen
  // ==========================================
  
  return (
    <div className="view-patients-container">
      {/* Navigation Bar */}
      <nav className="patients-nav">
        <div className="nav-left">
          <button onClick={() => navigate('/dashboard')} className="back-button">
            ← Back to Dashboard
          </button>
          <h1>🐾 Patients</h1>
        </div>
        <div className="nav-right">
          <span className="user-info">👤 {user?.email}</span>
        </div>
      </nav>

      <main className="patients-main">
        {/* Header with Search and Actions */}
        <div className="patients-header">
          <div className="search-box">
            <input
              type="text"
              placeholder="🔍 Search by pet name, owner, species, or breed..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>
          <button className="add-patient-button" onClick={() => navigate('/patients/new')}>
            + Add New Patient
          </button>
        </div>

        {/* CONDITIONAL RENDERING - Show different content based on state */}
        
        {/* Show loading spinner while fetching data */}
        {isLoading && (
          <div className="loading-state">
            <p>Loading patients... 🔄</p>
          </div>
        )}

        {/* Show error message if something went wrong */}
        {error && !isLoading && (
          <div className="error-state">
            <p>❌ {error}</p>
            <button onClick={fetchPatients} className="retry-button">
              Try Again
            </button>
          </div>
        )}

        {/* Show empty state if no patients */}
        {!isLoading && !error && filteredPatients.length === 0 && (
          <div className="empty-state">
            <p>📋 {searchQuery ? 'No patients found matching your search' : 'No patients yet'}</p>
            {!searchQuery && (
              <button onClick={() => navigate('/patients/new')} className="add-first-button">
                Add Your First Patient
              </button>
            )}
          </div>
        )}

        {/* Show patients table when data is loaded */}
        {!isLoading && !error && filteredPatients.length > 0 && (
          <div className="patients-table-container">
            <table className="patients-table">
              <thead>
                <tr>
                  <th>Pet Name</th>
                  <th>Species</th>
                  <th>Breed</th>
                  <th>Age</th>
                  <th>Owner</th>
                  <th>Contact</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {/* Loop through each patient and create a table row */}
                {filteredPatients.map((patient) => (
                  <tr key={patient.id} className="patient-row">
                    <td className="pet-name">
                      <strong>{patient.pet_name}</strong>
                      {patient.gender && (
                        <span className="gender-badge">
                          {patient.gender === 'male' ? '♂' : patient.gender === 'female' ? '♀' : '?'}
                        </span>
                      )}
                    </td>
                    <td>
                      <span className="species-badge">{patient.species}</span>
                    </td>
                    <td>{patient.breed || 'N/A'}</td>
                    <td>{calculateAge(patient.date_of_birth)}</td>
                    <td>
                      {patient.owner_first_name} {patient.owner_last_name}
                    </td>
                    <td>
                      {patient.owner_phone && (
                        <div className="contact-info">
                          📞 {patient.owner_phone}
                        </div>
                      )}
                      {patient.owner_email && (
                        <div className="contact-info">
                          ✉️ {patient.owner_email}
                        </div>
                      )}
                    </td>
                    <td>
                      <button
                        onClick={() => handleViewPatient(patient.id)}
                        className="view-button"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            {/* Summary */}
            <div className="patients-summary">
              Showing {filteredPatients.length} of {patients.length} patients
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default ViewPatientsPage;
