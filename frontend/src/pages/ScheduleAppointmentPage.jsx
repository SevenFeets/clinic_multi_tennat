import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { createAppointment } from '../services/appointmentService';
import { getPatients } from '../services/patientService';
import '../styles/ScheduleAppointmentPage.css';

/**
 * ScheduleAppointmentPage Component
 * 
 * This page allows users to schedule a new appointment.
 */

function ScheduleAppointmentPage() {
    const { user } = useAuth();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        patient_id: '',
        appointment_date: '',
        appointment_time: '',
        duration_minutes: 30,
        notes: '',
        diagnosis: '',
        medicine_given: '',
    });

    const [patients, setPatients] = useState([]);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isLoadingPatients, setIsLoadingPatients] = useState(true);

    // Fetch patients on component mount
    useEffect(() => {
        const fetchPatients = async () => {
            try {
                setIsLoadingPatients(true);
                const data = await getPatients();
                setPatients(data);
            } catch (err) {
                console.error('Error fetching patients:', err);
                setError('Failed to load patients. Please refresh the page.');
            } finally {
                setIsLoadingPatients(false);
            }
        };
        fetchPatients();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
        setError('');
    };

    const validateForm = () => {
        if (!formData.patient_id) {
            setError('Patient is required');
            return false;
        }
        if (!formData.appointment_date) {
            setError('Appointment date is required');
            return false;
        }
        if (!formData.appointment_time) {
            setError('Appointment time is required');
            return false;
        }
        if (!formData.duration_minutes) {
            setError('Duration is required');
            return false;
        }

        // Validate that appointment is in the future
        const appointmentDateTime = new Date(`${formData.appointment_date}T${formData.appointment_time}`);
        const now = new Date();
        if (appointmentDateTime <= now) {
            setError('Appointment must be scheduled for a future date and time');
            return false;
        }

        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Validate form
        if (!validateForm()) {
            return;
        }

        setIsLoading(true);
        try {
            // Combine date and time into ISO datetime string
            const appointmentDateTime = new Date(`${formData.appointment_date}T${formData.appointment_time}`);
            const isoDateTime = appointmentDateTime.toISOString();

            // Prepare appointment data with proper types
            const appointmentData = {
                patient_id: parseInt(formData.patient_id),
                appointment_time: isoDateTime,
                duration_minutes: parseInt(formData.duration_minutes),
                notes: formData.notes || null,
                diagnosis: formData.diagnosis || null,
                medicine_given: formData.medicine_given || null,
            };

            await createAppointment(appointmentData);
            navigate('/today-appointments');
        } catch (err) {
            console.error('Error scheduling appointment:', err);
            // Extract error message from response
            const errorMessage = err.response?.data?.detail || err.message || 'Failed to schedule appointment. Please try again.';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCancel = () => {
        navigate('/dashboard');
    };

    return (
        <div className="schedule-appointment-container">
            {/* Navigation Bar */}
            <nav className="schedule-appointment-nav">
                <div className="nav-left">
                    <button onClick={handleCancel} className="back-button">
                        ← Back to Appointments
                    </button>
                    <h1>📅 Schedule Appointment</h1>
                </div>
                <div className="nav-right">
                    <span className="user-info">👤 {user?.first_name || user?.email}</span>
                </div>
            </nav>

            {/* Main Content */}
            <main className="schedule-appointment-main">
                <div className="form-container">
                    <form onSubmit={handleSubmit} className="appointment-form">
                        {/* Error Message */}
                        {error && (
                            <div className="error-message">
                                ❌ {error}
                            </div>
                        )}

                        {/* Patient Selection Section */}
                        <section className="form-section">
                            <h2>🐾 Select Patient</h2>
                            
                            <div className="form-group required">
                                <label htmlFor="patient_id">Patient *</label>
                                <select
                                    id="patient_id"
                                    name="patient_id"
                                    value={formData.patient_id}
                                    onChange={handleChange}
                                    required
                                    disabled={isLoadingPatients}
                                >
                                    <option value="">
                                        {isLoadingPatients ? 'Loading patients...' : 'Select a patient'}
                                    </option>
                                    {patients.map((patient) => (
                                        <option key={patient.id} value={patient.id}>
                                            {patient.pet_name} ({patient.species}) - Owner: {patient.owner_full_name}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </section>

                        {/* Appointment Details Section */}
                        <section className="form-section">
                            <h2>📅 Appointment Details</h2>
                            
                            <div className="form-row">
                                <div className="form-group required">
                                    <label htmlFor="appointment_date">Date *</label>
                                    <input
                                        type="date"
                                        id="appointment_date"
                                        name="appointment_date"
                                        value={formData.appointment_date}
                                        onChange={handleChange}
                                        min={new Date().toISOString().split('T')[0]}
                                        required
                                    />
                                </div>

                                <div className="form-group required">
                                    <label htmlFor="appointment_time">Time *</label>
                                    <input
                                        type="time"
                                        id="appointment_time"
                                        name="appointment_time"
                                        value={formData.appointment_time}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>

                            <div className="form-group required">
                                <label htmlFor="duration_minutes">Duration (minutes) *</label>
                                <select
                                    id="duration_minutes"
                                    name="duration_minutes"
                                    value={formData.duration_minutes}
                                    onChange={handleChange}
                                    required
                                >
                                    <option value="15">15 minutes</option>
                                    <option value="30">30 minutes</option>
                                    <option value="45">45 minutes</option>
                                    <option value="60">60 minutes</option>
                                </select>
                            </div>
                        </section>

                        {/* Additional Notes Section */}
                        <section className="form-section">
                            <h2>📝 Additional Information</h2>
                            
                            <div className="form-group">
                                <label htmlFor="notes">Notes</label>
                                <textarea
                                    id="notes"
                                    name="notes"
                                    value={formData.notes}
                                    onChange={handleChange}
                                    placeholder="Any additional notes about this appointment"
                                    rows="3"
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="diagnosis">Diagnosis</label>
                                <textarea
                                    id="diagnosis"
                                    name="diagnosis"
                                    value={formData.diagnosis}
                                    onChange={handleChange}
                                    placeholder="Diagnosis or reason for visit"
                                    rows="3"
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="medicine_given">Medicine Given</label>
                                <textarea
                                    id="medicine_given"
                                    name="medicine_given"
                                    value={formData.medicine_given}
                                    onChange={handleChange}
                                    placeholder="Medications prescribed or administered"
                                    rows="2"
                                />
                            </div>
                        </section>

                        {/* Form Actions */}
                        <div className="form-actions">
                            <button
                                type="button"
                                onClick={handleCancel}
                                className="btn btn-cancel"
                                disabled={isLoading}
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                className="btn btn-submit"
                                disabled={isLoading || isLoadingPatients}
                            >
                                {isLoading ? 'Scheduling...' : 'Schedule Appointment'}
                            </button>
                        </div>
                    </form>
                </div>
            </main>
        </div>
    );
}

export default ScheduleAppointmentPage;
