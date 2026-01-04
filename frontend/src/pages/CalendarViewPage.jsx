import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAppointments } from '../services/appointmentService';
import '../styles/CalendarViewPage.css';

function CalendarViewPage() {
    // Get user info for navigation
    const navigate = useNavigate();

    // Localizer using moment.js
    const localizer = momentLocalizer(moment);

    // state management
    const [appointments, setAppointments] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [view, setView] = useState('month');
    const [selectedDate, setSelectedDate] = useState(new Date());
    

    // Fetch appointments when component mounts
    useEffect(() => {
        fetchAppointments();
    }, []);

    const fetchAppointments = async () => {
        try {
            setIsLoading(true);
            setError(null);
            const data = await getAppointments();
            setAppointments(data);
        } catch (err) {
            console.error('Error fetching appointments:', err);
            setError(err.message || 'Failed to load appointments');
        } finally {
            setIsLoading(false);
        }
    };


    // transform appointments to calendar events
    const events = appointments.map((appointment) => {
        const startTime = new Date(appointment.appointment_time);
        const endTime = new Date(startTime.getTime() + appointment.duration_minutes * 60000);
        return {
            id: appointment.id,
            start: startTime,
            end: endTime,
            title: appointment.patient?.pet_name || 'Patient',
            description: appointment.notes,
            resource: appointment, // Store full appointment data
        };
    });

    // Handle event click - show appointment details
    const handleSelectEvent = (event) => {
        // Navigate to appointment details or show modal
        console.log('Selected appointment:', event.resource);
        // optional: detail page or show a modal = > navigate(`/appointments/${event.id}`);
    };

    // Handle empty slot click - create new appointment
    const handleSelectSlot = ({ start }) => {
        // Navigate to schedule appointment page with pre-filled date/time
        const dateStr = start.toISOString().split('T')[0];
        const timeStr = start.toTimeString().slice(0, 5);
        navigate('/schedule-appointment', { 
            state: { 
                date: dateStr, 
                time: timeStr 
            } 
        });
    };

    // Color code events by status
    const eventPropGetter = (event) => {
        const status = event.resource?.status || 'scheduled';
        const colors = {
            scheduled: { backgroundColor: '#3182ce', color: 'white' },
            completed: { backgroundColor: '#38a169', color: 'white' },
            cancelled: { backgroundColor: '#e53e3e', color: 'white' },
            no_show: { backgroundColor: '#d69e2e', color: 'white' }
        };
        return {
            style: colors[status] || { backgroundColor: '#718096', color: 'white' }
        };
    };

    return (
        <div className="calendar-view-page">
            <div className="calendar-header">
                <h1>📅 Calendar View</h1>
                <div className="calendar-controls">
                    <button onClick={() => setSelectedDate(new Date())}>
                        Today
                    </button>
                </div>
            </div>
            
            {isLoading ? (
                <p>Loading appointments...</p>
            ) : error ? (
                <p>Error: {error}</p>
            ) : (
                <div className="calendar-container">
                    <Calendar
                        localizer={localizer}
                        events={events}
                        startAccessor="start"
                        endAccessor="end"
                        view={view}
                        onView={setView}
                        date={selectedDate}
                        onNavigate={setSelectedDate}
                        onSelectEvent={handleSelectEvent}
                        onSelectSlot={handleSelectSlot}
                        selectable
                        eventPropGetter={eventPropGetter}
                        style={{ height: '600px' }}
                    />
                </div>
            )}
        </div>
    );

}

export default CalendarViewPage;