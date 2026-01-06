import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { createPatient } from '../services/patientService';
import '../styles/NewPatientPage.css';

/**
 * NewPatientPage Component
 * 
 * Form to register a new patient (pet) in the clinic.
 * Includes pet information, owner information, and medical history.
 */

function NewPatientPage() {
    const { user } = useAuth();
    const navigate = useNavigate();

    // Form state - all fields from PatientCreate schema
    const [formData, setFormData] = useState({
        // Pet Information (Required)
        pet_name: '',
        species: '',
        // Pet Information (Optional)
        breed: '',
        color: '',
        gender: '',
        date_of_birth: '',
        chip_number: '',
        weight: '',
        
        // Owner Information (Required)
        owner_first_name: '',
        owner_last_name: '',
        // Owner Information (Optional)
        owner_email: '',
        owner_phone: '',
        owner_address: '',
        
        // Medical Information (Optional)
        medical_history: '',
        allergies: '',
        special_notes: '',
    });

    // UI state
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    /**
     * Handle input changes
     */
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
        // Clear error when user starts typing
        setError('');
    };

    /**
     * Validate form before submission
     */
    const validateForm = () => {
        // Required fields
        if (!formData.pet_name.trim()) {
            setError('Pet name is required');
            return false;
        }
        if (!formData.species.trim()) {
            setError('Species is required');
            return false;
        }
        if (!formData.owner_first_name.trim()) {
            setError('Owner first name is required');
            return false;
        }
        if (!formData.owner_last_name.trim()) {
            setError('Owner last name is required');
            return false;
        }

        // Email validation (if provided)
        if (formData.owner_email && !formData.owner_email.includes('@')) {
            setError('Please enter a valid email address');
            return false;
        }

        // Weight validation (if provided)
        if (formData.weight && (isNaN(formData.weight) || parseFloat(formData.weight) <= 0)) {
            setError('Weight must be a positive number');
            return false;
        }

        return true;
    };

    /**
     * Handle form submission
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validate form
        if (!validateForm()) {
            return;
        }

        setIsLoading(true);
        setError('');

        try {
            // Prepare data for API (convert empty strings to null, convert weight to number)
            const patientData = {
                ...formData,
                // Convert empty strings to null for optional fields
                breed: formData.breed || null,
                color: formData.color || null,
                gender: formData.gender || null,
                date_of_birth: formData.date_of_birth || null,
                chip_number: formData.chip_number || null,
                weight: formData.weight ? parseFloat(formData.weight) : null,
                owner_email: formData.owner_email || null,
                owner_phone: formData.owner_phone || null,
                owner_address: formData.owner_address || null,
                medical_history: formData.medical_history || null,
                allergies: formData.allergies || null,
                special_notes: formData.special_notes || null,
            };

            // Create patient
            await createPatient(patientData);
            
            // Success! Redirect to patients list
            navigate('/patients');
        } catch (err) {
            console.error('Error creating patient:', err);
            setError(err.message || 'Failed to create patient. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Handle cancel - go back
     */
    const handleCancel = () => {
        navigate('/patients');
    };

    return (
        <div className="new-patient-container">
            {/* Navigation Bar */}
            <nav className="new-patient-nav">
                <div className="nav-left">
                    <button onClick={handleCancel} className="back-button">
                        ← Back to Patients
                    </button>
                    <h1>🐾 Register New Patient</h1>
                </div>
                <div className="nav-right">
                    <span className="user-info">👤 {user?.first_name || user?.email}</span>
                </div>
            </nav>

            {/* Main Content */}
            <main className="new-patient-main">
                <div className="form-container">
                    <form onSubmit={handleSubmit} className="patient-form">
                        {/* Error Message */}
                        {error && (
                            <div className="error-message">
                                ❌ {error}
                            </div>
                        )}

                        {/* Pet Information Section */}
                        <section className="form-section">
                            <h2>🐾 Pet Information</h2>
                            
                            <div className="form-row">
                                <div className="form-group required">
                                    <label htmlFor="pet_name">Pet Name *</label>
                                    <input
                                        type="text"
                                        id="pet_name"
                                        name="pet_name"
                                        value={formData.pet_name}
                                        onChange={handleChange}
                                        placeholder="e.g., Max, Bella"
                                        required
                                    />
                                </div>

                                <div className="form-group required">
                                    <label htmlFor="species">Species *</label>
                                    <select
                                        id="species"
                                        name="species"
                                        value={formData.species}
                                        onChange={handleChange}
                                        required
                                    >
                                        <option value="">Select species</option>
                                        <option value="dog">Dog</option>
                                        <option value="cat">Cat</option>
                                        <option value="bird">Bird</option>
                                        <option value="rabbit">Rabbit</option>
                                        <option value="hamster">Hamster</option>
                                        <option value="guinea_pig">Guinea Pig</option>
                                        <option value="reptile">Reptile</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label htmlFor="breed">Breed</label>
                                    <input
                                        type="text"
                                        id="breed"
                                        name="breed"
                                        value={formData.breed}
                                        onChange={handleChange}
                                        placeholder="e.g., Golden Retriever"
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="color">Color</label>
                                    <input
                                        type="text"
                                        id="color"
                                        name="color"
                                        value={formData.color}
                                        onChange={handleChange}
                                        placeholder="e.g., Golden, Black"
                                    />
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label htmlFor="gender">Gender</label>
                                    <select
                                        id="gender"
                                        name="gender"
                                        value={formData.gender}
                                        onChange={handleChange}
                                    >
                                        <option value="">Select gender</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                        <option value="unknown">Unknown</option>
                                    </select>
                                </div>

                                <div className="form-group">
                                    <label htmlFor="date_of_birth">Date of Birth</label>
                                    <input
                                        type="date"
                                        id="date_of_birth"
                                        name="date_of_birth"
                                        value={formData.date_of_birth}
                                        onChange={handleChange}
                                    />
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label htmlFor="chip_number">Microchip Number</label>
                                    <input
                                        type="text"
                                        id="chip_number"
                                        name="chip_number"
                                        value={formData.chip_number}
                                        onChange={handleChange}
                                        placeholder="9-15 digits"
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="weight">Weight (kg)</label>
                                    <input
                                        type="number"
                                        id="weight"
                                        name="weight"
                                        value={formData.weight}
                                        onChange={handleChange}
                                        placeholder="e.g., 25.5"
                                        min="0"
                                        step="0.1"
                                    />
                                </div>
                            </div>
                        </section>

                        {/* Owner Information Section */}
                        <section className="form-section">
                            <h2>👤 Owner Information</h2>
                            
                            <div className="form-row">
                                <div className="form-group required">
                                    <label htmlFor="owner_first_name">First Name *</label>
                                    <input
                                        type="text"
                                        id="owner_first_name"
                                        name="owner_first_name"
                                        value={formData.owner_first_name}
                                        onChange={handleChange}
                                        placeholder="Owner's first name"
                                        required
                                    />
                                </div>

                                <div className="form-group required">
                                    <label htmlFor="owner_last_name">Last Name *</label>
                                    <input
                                        type="text"
                                        id="owner_last_name"
                                        name="owner_last_name"
                                        value={formData.owner_last_name}
                                        onChange={handleChange}
                                        placeholder="Owner's last name"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label htmlFor="owner_email">Email</label>
                                    <input
                                        type="email"
                                        id="owner_email"
                                        name="owner_email"
                                        value={formData.owner_email}
                                        onChange={handleChange}
                                        placeholder="owner@example.com"
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="owner_phone">Phone</label>
                                    <input
                                        type="tel"
                                        id="owner_phone"
                                        name="owner_phone"
                                        value={formData.owner_phone}
                                        onChange={handleChange}
                                        placeholder="10-15 digits"
                                    />
                                </div>
                            </div>

                            <div className="form-group">
                                <label htmlFor="owner_address">Address</label>
                                <textarea
                                    id="owner_address"
                                    name="owner_address"
                                    value={formData.owner_address}
                                    onChange={handleChange}
                                    placeholder="Owner's full address"
                                    rows="2"
                                />
                            </div>
                        </section>

                        {/* Medical Information Section */}
                        <section className="form-section">
                            <h2>🏥 Medical Information</h2>
                            
                            <div className="form-group">
                                <label htmlFor="medical_history">Medical History</label>
                                <textarea
                                    id="medical_history"
                                    name="medical_history"
                                    value={formData.medical_history}
                                    onChange={handleChange}
                                    placeholder="Previous medical conditions, surgeries, etc."
                                    rows="3"
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="allergies">Allergies</label>
                                <textarea
                                    id="allergies"
                                    name="allergies"
                                    value={formData.allergies}
                                    onChange={handleChange}
                                    placeholder="Known allergies or reactions"
                                    rows="2"
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="special_notes">Special Notes</label>
                                <textarea
                                    id="special_notes"
                                    name="special_notes"
                                    value={formData.special_notes}
                                    onChange={handleChange}
                                    placeholder="Special care instructions or notes"
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
                                disabled={isLoading}
                            >
                                {isLoading ? 'Creating...' : 'Create Patient'}
                            </button>
                        </div>
                    </form>
                </div>
            </main>
        </div>
    );
}

export default NewPatientPage;