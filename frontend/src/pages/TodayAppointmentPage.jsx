import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getTodayAppointments } from '../services/appointmentService';
import '../styles/TodayAppointmentPage.css';

/**
 * TodayAppointmentPage Component
 * 
 * This page displays all appointments scheduled for today.
 */

function TodayAppointmentPage() {
    const { user } = useAuth();
    const navigate = useNavigate();

    const [todayAppointments, setTodayAppointments] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchTodayAppointments();
    }, []);

    const fetchTodayAppointments = async () => {
        try {
            setIsLoading(true);
            setError(null);

            // Call the API to get today's appointments
            const data = await getTodayAppointments();

            // Sort appointments by time (earliest first)
            const sorted = data.sort((a, b) => {
                return new Date(a.appointment_time) - new Date(b.appointment_time);
            });

            setTodayAppointments(sorted);
        } catch (err) {
            console.error('Error fetching today\'s appointments:', err);
            setError(err.message || 'Failed to load today\'s appointments');
        } finally {
            setIsLoading(false);
        }
    };

    // Format time for display
    const formatTime = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
    };

    // Format date for display
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            weekday: 'long',
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    };

    // Get status badge color
    const getStatusColor = (status) => {
        const colors = {
            scheduled: '#3182ce',
            completed: '#38a169',
            cancelled: '#e53e3e',
            no_show: '#d69e2e'
        };
        return colors[status] || '#718096';
    };

    // Get status emoji
    const getStatusEmoji = (status) => {
        const emojis = {
            scheduled: '📅',
            completed: '✅',
            cancelled: '❌',
            no_show: '⏰'
        };
        return emojis[status] || '📋';
    };

    return (
        <div className="today-appointments-container">
            {/* Navigation Bar */}
            <nav className="today-appointments-nav">
                <div className="nav-left">
                    <button onClick={() => navigate('/dashboard')} className="back-button">
                        ← Back to Dashboard
                    </button>
                    <h1>📅 Today's Appointments</h1>
                </div>
                <div className="nav-right">
                    <span className="user-info">👤 {user?.first_name || user?.email}</span>
                </div>
            </nav>

            {/* Main Content */}
            <main className="today-appointments-main">
                {/* Header Section */}
                <section className="header-section">
                    <h2>Today's Schedule</h2>
                    <p>
                        {todayAppointments.length === 0 
                            ? 'No appointments scheduled for today' 
                            : `${todayAppointments.length} ${todayAppointments.length === 1 ? 'appointment' : 'appointments'} scheduled`}
                    </p>
                </section>

                {/* Loading State */}
                {isLoading && (
                    <div className="loading-state">
                        <p>Loading appointments... ⏳</p>
                    </div>
                )}

                {/* Error State */}
                {error && !isLoading && (
                    <div className="error-state">
                        <p>❌ {error}</p>
                        <button onClick={fetchTodayAppointments} className="retry-button">
                            Try Again
                        </button>
                    </div>
                )}

                {/* Appointments List */}
                {!isLoading && !error && (
                    <>
                        {/* Summary Card */}
                        <div className="summary-card">
                            <div className="summary-icon">📊</div>
                            <div className="summary-content">
                                <h3>Total Appointments</h3>
                                <p className="summary-number">{todayAppointments.length}</p>
                                <p className="summary-description">
                                    {todayAppointments.length === 0 
                                        ? 'No appointments today' 
                                        : todayAppointments.filter(a => a.status === 'completed').length === todayAppointments.length
                                        ? 'All completed! 🎉'
                                        : `${todayAppointments.filter(a => a.status === 'completed').length} completed`}
                                </p>
                            </div>
                        </div>

                        {/* Appointments List */}
                        {todayAppointments.length === 0 ? (
                            <div className="empty-state">
                                <div className="empty-icon">📅</div>
                                <h3>No Appointments Today</h3>
                                <p>You have a free day! No appointments scheduled.</p>
                            </div>
                        ) : (
                            <div className="appointments-list">
                                {todayAppointments.map((appointment) => (
                                    <div key={appointment.id} className="appointment-card">
                                        <div className="appointment-time">
                                            <div className="time-display">
                                                {formatTime(appointment.appointment_time)}
                                            </div>
                                            <div className="duration">
                                                {appointment.duration_minutes || 30} min
                                            </div>
                                        </div>
                                        <div className="appointment-details">
                                            <div className="appointment-header">
                                                <h4>Patient ID: {appointment.patient_id}</h4>
                                                <span 
                                                    className="status-badge"
                                                    style={{ backgroundColor: getStatusColor(appointment.status) }}
                                                >
                                                    {getStatusEmoji(appointment.status)} {appointment.status}
                                                </span>
                                            </div>
                                            {appointment.notes && (
                                                <p className="appointment-notes">
                                                    📝 {appointment.notes}
                                                </p>
                                            )}
                                            {appointment.diagnosis && (
                                                <p className="appointment-diagnosis">
                                                    🩺 Diagnosis: {appointment.diagnosis}
                                                </p>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </>
                )}
            </main>
        </div>
    );
}

export default TodayAppointmentPage;