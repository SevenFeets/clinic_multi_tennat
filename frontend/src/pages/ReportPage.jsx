import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getPatients } from '../services/patientService';
import '../styles/ReportPage.css';

/**
 * ReportPage Component
 * 
 * Displays medical reports for each patient in the clinic.
 * Each patient gets their own report card showing:
 * - Patient information (pet name, species, breed, age)
 * - Owner information
 * - Medical history, allergies, and special notes
 * 
 * React Concepts Used:
 * - useState: Store patients data, loading state, errors
 * - useEffect: Fetch patients when page loads
 * - Conditional Rendering: Show different content based on state
 */

function ReportPage() {
    // Get user info for navigation
    const { user } = useAuth();
    const navigate = useNavigate();

    // State management
    const [patients, setPatients] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch patients when component mounts
    useEffect(() => {
        fetchReports();
    }, []);

    /**
     * Fetch all patients from the database
     * Each patient will be displayed as a report
     */
    const fetchReports = async () => {
        try {
            setIsLoading(true);
            setError(null);
            const data = await getPatients();
            setPatients(data);
        } catch (err) {
            console.error('Error fetching reports:', err);
            setError(err.message || 'Failed to load reports');
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Calculate pet's age from date of birth
     * @param {string} dateOfBirth - Pet's date of birth
     * @returns {string} Age in years or "Unknown"
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

    return (
        <div className="report-page-container">
            {/* Navigation Bar */}
            <nav className="report-nav">
                <div className="nav-left">
                    <button onClick={() => navigate('/dashboard')} className="back-button">
                        ← Back to Dashboard
                    </button>
                    <h1>📊 Patient Reports</h1>
                </div>
                <div className="nav-right">
                    <span className="user-info">👤 {user?.email}</span>
                </div>
            </nav>

            <main className="report-main">
                {/* Loading State */}
                {isLoading && (
                    <div className="loading-state">
                        <p>Loading patient reports... 🔄</p>
                    </div>
                )}

                {/* Error State */}
                {error && !isLoading && (
                    <div className="error-state">
                        <p>❌ {error}</p>
                        <button onClick={fetchReports} className="retry-button">
                            Try Again
                        </button>
                    </div>
                )}

                {/* Empty State */}
                {!isLoading && !error && patients.length === 0 && (
                    <div className="empty-state">
                        <p>📋 No patients found</p>
                        <p>Patient reports will appear here once you add patients to the system.</p>
                        <button onClick={() => navigate('/patients/new')} className="add-first-button">
                            Add Your First Patient
                        </button>
                    </div>
                )}

                {/* Reports Grid - Display each patient as a report card */}
                {!isLoading && !error && patients.length > 0 && (
                    <div className="reports-grid">
                        {patients.map((patient) => (
                            <div key={patient.id} className="report-card">
                                {/* Patient Header */}
                                <div className="report-header">
                                    <div className="patient-name-section">
                                        <h2>{patient.pet_name}</h2>
                                        {patient.gender && (
                                            <span className="gender-badge">
                                                {patient.gender === 'male' ? '♂' : patient.gender === 'female' ? '♀' : '?'}
                                            </span>
                                        )}
                                    </div>
                                    <span className="species-badge">{patient.species}</span>
                                </div>

                                {/* Patient Information */}
                                <div className="report-section">
                                    <h3>🐾 Patient Information</h3>
                                    <div className="info-grid">
                                        <div className="info-item">
                                            <span className="info-label">Breed:</span>
                                            <span className="info-value">{patient.breed || 'N/A'}</span>
                                        </div>
                                        <div className="info-item">
                                            <span className="info-label">Age:</span>
                                            <span className="info-value">{calculateAge(patient.date_of_birth)}</span>
                                        </div>
                                        {patient.weight && (
                                            <div className="info-item">
                                                <span className="info-label">Weight:</span>
                                                <span className="info-value">{patient.weight} kg</span>
                                            </div>
                                        )}
                                        {patient.color && (
                                            <div className="info-item">
                                                <span className="info-label">Color:</span>
                                                <span className="info-value">{patient.color}</span>
                                            </div>
                                        )}
                                        {patient.chip_number && (
                                            <div className="info-item">
                                                <span className="info-label">Chip #:</span>
                                                <span className="info-value">{patient.chip_number}</span>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* Owner Information */}
                                <div className="report-section">
                                    <h3>👤 Owner Information</h3>
                                    <div className="info-grid">
                                        <div className="info-item">
                                            <span className="info-label">Name:</span>
                                            <span className="info-value">
                                                {patient.owner_first_name} {patient.owner_last_name}
                                            </span>
                                        </div>
                                        {patient.owner_phone && (
                                            <div className="info-item">
                                                <span className="info-label">Phone:</span>
                                                <span className="info-value">{patient.owner_phone}</span>
                                            </div>
                                        )}
                                        {patient.owner_email && (
                                            <div className="info-item">
                                                <span className="info-label">Email:</span>
                                                <span className="info-value">{patient.owner_email}</span>
                                            </div>
                                        )}
                                        {patient.owner_address && (
                                            <div className="info-item full-width">
                                                <span className="info-label">Address:</span>
                                                <span className="info-value">{patient.owner_address}</span>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* Medical Information */}
                                <div className="report-section">
                                    <h3>🏥 Medical Information</h3>
                                    {patient.medical_history && (
                                        <div className="medical-item">
                                            <span className="medical-label">Medical History:</span>
                                            <p className="medical-text">{patient.medical_history}</p>
                                        </div>
                                    )}
                                    {patient.allergies && (
                                        <div className="medical-item">
                                            <span className="medical-label">Allergies:</span>
                                            <p className="medical-text allergies-warning">{patient.allergies}</p>
                                        </div>
                                    )}
                                    {patient.special_notes && (
                                        <div className="medical-item">
                                            <span className="medical-label">Special Notes:</span>
                                            <p className="medical-text">{patient.special_notes}</p>
                                        </div>
                                    )}
                                    {!patient.medical_history && !patient.allergies && !patient.special_notes && (
                                        <p className="no-medical-info">No medical information recorded yet.</p>
                                    )}
                                </div>

                                {/* Report Footer */}
                                <div className="report-footer">
                                    <span className="report-date">
                                        Patient ID: {patient.id}
                                    </span>
                                    <button 
                                        className="view-details-button"
                                        onClick={() => navigate(`/patients/${patient.id}`)}
                                    >
                                        View Full Details →
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

export default ReportPage;