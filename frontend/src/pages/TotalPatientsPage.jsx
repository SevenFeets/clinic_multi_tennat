import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getPatients } from '../services/patientService';
import '../styles/TotalPatientsPage.css';


/**
 * TotalPatientsPage Component
 * 
 * This page displays the total number of patients in the clinic.
 * 
 * React Concepts Used:
 * - useState: To store data that can change (patients list, loading state, errors)
 * - useEffect: To fetch data when the page loads
 * - Conditional Rendering: Show different content based on state
 */

function TotalPatientsPage() {

    // 1. HOOKS - These manage the component's state and side effects
    // Get the current logged-in user info
    const { user } = useAuth();

    const navigate = useNavigate();
    // useState creates a piece of state (data that can change)
    const [totalPatients, setTotalPatients] = useState(0);

    // Track if we're currently loading data
    const [isLoading, setIsLoading] = useState(true);

    // Store any error messages
    const [error, setError] = useState(null);

    // 2. FETCH DATA - Load total patients when page loads
    // useEffect runs code when the component mounts (appears on screen)
    // The empty [] means "run once when page loads"
    useEffect(() => {
        fetchTotalPatients();
    }, []); // Empty array = run once on mount
    
    
    const fetchTotalPatients = async () => {
        try {
            setIsLoading(true);
            setError(null);

            // Call the API to get total patients
            const data = await getPatients();

            // Update state with the fetched data
            setTotalPatients(data.length);
        } catch (err) {
            console.error('Error fetching total patients:', err);
            setError(err.message || 'Failed to load total patients');
        } finally {
            setIsLoading(false);
        }
    };


    // 3. RENDERING - Show the data to the user
    return (
        <div className="total-patients-container">
            {/* Navigation Bar */}
            <nav className="total-patients-nav">
                <div className="nav-left">
                    <button onClick={() => navigate('/dashboard')} className="back-button">
                        ← Back to Dashboard
                    </button>
                    <h1>🐾 Total Patients</h1>
                </div>
                <div className="nav-right">
                    <span className="user-info">👤 {user?.email}</span>
                </div>
            </nav>

            {/* Main Content */}
            <main className="total-patients-main">
                {/* Header Section */}
                <section className="header-section">
                    <h2>Patient Statistics</h2>
                    <p>Overview of all patients in your clinic</p>
                </section>

                {/* CONDITIONAL RENDERING - Show different content based on state */}
                
                {/* Show loading spinner while fetching data */}
                {isLoading && (
                    <div className="loading-state">
                        <p>Loading patient statistics... 🔄</p>
                    </div>
                )}

                {/* Show error message if something went wrong */}
                {error && !isLoading && (
                    <div className="error-state">
                        <p>❌ {error}</p>
                        <button onClick={fetchTotalPatients} className="retry-button">
                            Try Again
                        </button>
                    </div>
                )}

                {/* Show total patients when data is loaded */}
                {!isLoading && !error && (
                    <section className="stats-section">
                        {/* Main Total Patients Card */}
                        <div className="total-card">
                            <div className="card-icon">🐾</div>
                            <div className="card-content">
                                <h3>Total Patients</h3>
                                <p className="total-number">{totalPatients}</p>
                                <p className="card-description">
                                    {totalPatients === 0 
                                        ? 'No patients registered yet' 
                                        : totalPatients === 1 
                                        ? 'patient in your clinic' 
                                        : 'patients in your clinic'}
                                </p>
                            </div>
                        </div>

                        {/* Additional Info Card */}
                        <div className="info-card">
                            <h4>Quick Actions</h4>
                            <div className="action-buttons">
                                <button 
                                    onClick={() => navigate('/patients')} 
                                    className="action-btn"
                                >
                                    View All Patients
                                </button>
                                <button 
                                    onClick={() => navigate('/patients/new')} 
                                    className="action-btn primary"
                                >
                                    + Add New Patient
                                </button>
                            </div>
                        </div>
                    </section>
                )}
            </main>
        </div>
    );
}

export default TotalPatientsPage;