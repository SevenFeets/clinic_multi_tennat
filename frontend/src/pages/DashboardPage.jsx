import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getDashboardStats } from '../services/statsService';
import '../styles/DashboardPage.css';

/**
 * DashboardPage Component
 * 
 * This is the main page users see after logging in.
 * It shows:
 * - Welcome message with user's name
 * - Quick stats (patients, appointments) - FETCHED FROM DATABASE
 * - Navigation to different sections
 * - Logout button
 */

function DashboardPage() {
  // Get user info and logout function from context
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // State for dashboard stats
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Fetch dashboard stats on component mount
   */
  useEffect(() => {
    const fetchStats = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await getDashboardStats();
        setStats(data);
      } catch (err) {
        console.error('Error loading dashboard stats:', err);
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []); // Empty dependency array = run once on mount

  /**
   * Handle logout
   * Logs user out and redirects to login page
   */
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      {/* Top Navigation Bar */}
      <nav className="dashboard-nav">
        <div className="nav-brand">
          <h2>🐾 Veterinary Clinic</h2>
        </div>
        <div className="nav-actions">
          <span className="user-name">👤 {user?.first_name || user?.email}</span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="dashboard-main">
        {/* Welcome Section */}
        <section className="welcome-section">
          <h1>Welcome back, {user?.first_name || 'Doctor'}! 👋</h1>
          <p>Here's what's happening in your clinic today</p>
        </section>

        {/* Stats Cards */}
        <section className="stats-section">
          {/* Show loading state */}
          {isLoading && (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '40px' }}>
              <p>Loading dashboard data... ⏳</p>
            </div>
          )}

          {/* Show error state */}
          {error && !isLoading && (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '40px' }}>
              <p style={{ color: '#e53e3e' }}>❌ {error}</p>
              <button 
                onClick={() => window.location.reload()} 
                style={{ marginTop: '10px', padding: '8px 16px', cursor: 'pointer' }}
              >
                Retry
              </button>
            </div>
          )}

          {/* Show stats when loaded */}
          {!isLoading && !error && stats && (
            <>
              <div className="stat-card" onClick={() => navigate('/total-patients')}>
                <div className="stat-icon">🐾</div>
                <div className="stat-content">
                  <h3>Total Patients</h3>
                  <p className="stat-number">{stats.total_patients}</p>
                  <p className="stat-change">+{stats.patients_this_month} this month</p>
                </div>
              </div>

              <div className="stat-card" onClick={() => navigate('/today-appointments')}>
                <div className="stat-icon">📅</div>
                <div className="stat-content">
                  <h3>Today's Appointments</h3>
                  <p className="stat-number">{stats.today_appointments}</p>
                  <p className="stat-change">{stats.today_completed} completed</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">⏰</div>
                <div className="stat-content">
                  <h3>Pending Appointments</h3>
                  <p className="stat-number">{stats.pending_appointments}</p>
                  <p className="stat-change">Scheduled</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">💰</div>
                <div className="stat-content">
                  <h3>Revenue</h3>
                  <p className="stat-number">${stats.revenue_this_month.toLocaleString()}</p>
                  <p className="stat-change">This month</p>
                </div>
              </div>
            </>
          )}
        </section>

        {/* Quick Actions */}
        <section className="actions-section">
          <h2>Quick Actions</h2>
          <div className="action-cards">
            <button className="action-card" onClick={() => navigate('/patients/new')}>
              <span className="action-icon">🐶</span>
              <span className="action-title">New Patient</span>
              <span className="action-description">Register a new patient</span>
            </button>

            <button className="action-card">
              <span className="action-icon">📅</span>
              <span className="action-title">Schedule Appointment</span>
              <span className="action-description">Book a new appointment</span>
            </button>

            <button className="action-card" onClick={() => navigate('/patients')}>
              <span className="action-icon">🐾</span>
              <span className="action-title">View Patients</span>
              <span className="action-description">See all patient records</span>
            </button>

            <button className="action-card">
              <span className="action-icon">📊</span>
              <span className="action-title">Reports</span>
              <span className="action-description">View clinic analytics</span>
            </button>
          </div>
        </section>

        {/* Recent Activity */}
        <section className="activity-section">
          <h2>Recent Activity</h2>
          <div className="activity-list">
            <div className="activity-item">
              <div className="activity-icon">✅</div>
              <div className="activity-content">
                <p className="activity-title">Appointment completed</p>
                <p className="activity-time">John Doe - 2 hours ago</p>
              </div>
            </div>

            <div className="activity-item">
              <div className="activity-icon">📝</div>
              <div className="activity-content">
                <p className="activity-title">New patient registered</p>
                <p className="activity-time">Jane Smith - 3 hours ago</p>
              </div>
            </div>

            <div className="activity-item">
              <div className="activity-icon">📅</div>
              <div className="activity-content">
                <p className="activity-title">Appointment scheduled</p>
                <p className="activity-time">Mike Johnson - 5 hours ago</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default DashboardPage;

