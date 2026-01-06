import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getDashboardStats, getAppointmentStats } from '../services/statsService';
import '../styles/AnalyticsPage.css';

function AnalyticsPage() {
    const { user } = useAuth();
    const navigate = useNavigate();

    const [dashboardStats, setDashboardStats] = useState(null);
    const [appointmentStats, setAppointmentStats] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            setIsLoading(true);
            setError(null);
            
            const [dashboardData, appointmentData] = await Promise.all([
                getDashboardStats(),
                getAppointmentStats()
            ]); 
            
            // dashboardData contains: total_patients, revenue_this_month, etc.
            // appointmentData contains: total_appointments, no_show_rate, etc.
            setDashboardStats(dashboardData);
            setAppointmentStats(appointmentData);
        } catch (err) {
            console.error('Error fetching analytics:', err);
            setError(err.message || 'Failed to load analytics data');
        } finally {
            setIsLoading(false);
        }
    };

    const formatCurrency = (value) => {
        if (value == null) return 'N/A';
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(value);
    };

    const formatNumber = (value) => {
        if (value == null) return 'N/A';
        return new Intl.NumberFormat('en-US').format(value);
    };

    const formatPercentage = (value) => {
        if (value == null) return 'N/A';
        return `${value.toFixed(1)}%`;
    };

    return (
        <div className="analytics-page">
            <nav className="analytics-nav">
                <button className="nav-back-btn" onClick={() => navigate('/dashboard')}>
                    ← Back to Dashboard
                </button>
                <h1>📊 Reports & Analytics</h1>
                <span className="user-email">{user?.email}</span>
            </nav>

            {isLoading && (
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading analytics data...</p>
                </div>
            )}

            {error && !isLoading && (
                <div className="error-container">
                    <div className="error-icon">⚠️</div>
                    <div className="error-content">
                        <h3>Error Loading Data</h3>
                        <p>{error}</p>
                        <button className="retry-btn" onClick={fetchStats}>
                            Retry
                        </button>
                    </div>
                </div>
            )}

            {!isLoading && !error && dashboardStats && appointmentStats && (
                <main className="analytics-content">
                    <div className="stats-grid">
                        <div className="stat-card stat-card-primary">
                            <div className="stat-icon">👥</div>
                            <div className="stat-content">
                                <h3>Total Patients</h3>
                                <p className="stat-value">{formatNumber(dashboardStats.total_patients)}</p>
                                {dashboardStats.patients_this_month > 0 && (
                                    <span className="stat-subtext">
                                        +{formatNumber(dashboardStats.patients_this_month)} this month
                                    </span>
                                )}
                            </div>
                        </div>

                        <div className="stat-card stat-card-success">
                            <div className="stat-icon">💰</div>
                            <div className="stat-content">
                                <h3>Revenue This Month</h3>
                                <p className="stat-value">{formatCurrency(dashboardStats.revenue_this_month)}</p>
                            </div>
                        </div>

                        <div className="stat-card stat-card-info">
                            <div className="stat-icon">📅</div>
                            <div className="stat-content">
                                <h3>Today's Appointments</h3>
                                <p className="stat-value">{formatNumber(dashboardStats.today_appointments)}</p>
                                {dashboardStats.today_completed > 0 && (
                                    <span className="stat-subtext">
                                        {formatNumber(dashboardStats.today_completed)} completed
                                    </span>
                                )}
                            </div>
                        </div>

                        <div className="stat-card stat-card-warning">
                            <div className="stat-icon">⏳</div>
                            <div className="stat-content">
                                <h3>Pending Appointments</h3>
                                <p className="stat-value">{formatNumber(dashboardStats.pending_appointments)}</p>
                            </div>
                        </div>
                    </div>

                    <div className="stats-sections">
                        <section className="stats-section">
                            <h2>Appointment Overview</h2>
                            <div className="stats-details">
                                <div className="detail-item">
                                    <span className="detail-label">Total Appointments</span>
                                    <span className="detail-value">{formatNumber(appointmentStats.total_appointments)}</span>
                                </div>
                                <div className="detail-item">
                                    <span className="detail-label">No Show Rate</span>
                                    <span className="detail-value">{formatPercentage(appointmentStats.no_show_rate)}</span>
                                </div>
                                <div className="detail-item">
                                    <span className="detail-label">Average Duration</span>
                                    <span className="detail-value">
                                        {appointmentStats.average_duration_minutes != null 
                                            ? `${appointmentStats.average_duration_minutes.toFixed(1)} min`
                                            : 'N/A'}
                                    </span>
                                </div>
                                <div className="detail-item">
                                    <span className="detail-label">This Month</span>
                                    <span className="detail-value">{formatNumber(appointmentStats.appointments_this_month)}</span>
                                </div>
                                <div className="detail-item">
                                    <span className="detail-label">This Week</span>
                                    <span className="detail-value">{formatNumber(appointmentStats.appointments_this_week)}</span>
                                </div>
                                <div className="detail-item">
                                    <span className="detail-label">Upcoming</span>
                                    <span className="detail-value">{formatNumber(appointmentStats.upcoming_appointments)}</span>
                                </div>
                            </div>
                        </section>

                        <section className="stats-section">
                            <h2>Status Breakdown</h2>
                            <div className="status-breakdown">
                                <div className="status-item status-completed">
                                    <div className="status-header">
                                        <span className="status-label">Completed</span>
                                        <span className="status-count">{formatNumber(appointmentStats.completed_count)}</span>
                                    </div>
                                    <div className="status-bar">
                                        <div 
                                            className="status-bar-fill status-fill-completed"
                                            style={{ 
                                                width: `${appointmentStats.total_appointments > 0 
                                                    ? (appointmentStats.completed_count / appointmentStats.total_appointments * 100) 
                                                    : 0}%` 
                                            }}
                                        ></div>
                                    </div>
                                </div>

                                <div className="status-item status-scheduled">
                                    <div className="status-header">
                                        <span className="status-label">Scheduled</span>
                                        <span className="status-count">{formatNumber(appointmentStats.scheduled_count)}</span>
                                    </div>
                                    <div className="status-bar">
                                        <div 
                                            className="status-bar-fill status-fill-scheduled"
                                            style={{ 
                                                width: `${appointmentStats.total_appointments > 0 
                                                    ? (appointmentStats.scheduled_count / appointmentStats.total_appointments * 100) 
                                                    : 0}%` 
                                            }}
                                        ></div>
                                    </div>
                                </div>

                                <div className="status-item status-cancelled">
                                    <div className="status-header">
                                        <span className="status-label">Cancelled</span>
                                        <span className="status-count">{formatNumber(appointmentStats.cancelled_count)}</span>
                                    </div>
                                    <div className="status-bar">
                                        <div 
                                            className="status-bar-fill status-fill-cancelled"
                                            style={{ 
                                                width: `${appointmentStats.total_appointments > 0 
                                                    ? (appointmentStats.cancelled_count / appointmentStats.total_appointments * 100) 
                                                    : 0}%` 
                                            }}
                                        ></div>
                                    </div>
                                </div>

                                <div className="status-item status-no-show">
                                    <div className="status-header">
                                        <span className="status-label">No Show</span>
                                        <span className="status-count">{formatNumber(appointmentStats.no_show_count)}</span>
                                    </div>
                                    <div className="status-bar">
                                        <div 
                                            className="status-bar-fill status-fill-no-show"
                                            style={{ 
                                                width: `${appointmentStats.total_appointments > 0 
                                                    ? (appointmentStats.no_show_count / appointmentStats.total_appointments * 100) 
                                                    : 0}%` 
                                            }}
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                </main>
            )}
        </div>
    );
}

export default AnalyticsPage;
