import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ProtectedRoute from './components/auth/ProtectedRoute';
import './App.css';

/**
 * App Component - The Root of Your Application
 * 
 * This is the main component that:
 * 1. Wraps everything in AuthProvider (for authentication state)
 * 2. Sets up routing with BrowserRouter
 * 3. Defines all the pages/routes in your app
 * 
 * Current Routes:
 * - / → Redirects to /login
 * - /login → Login page (public)
 * - /dashboard → Dashboard page (protected - requires login)
 */

function App() {
  return (
    // AuthProvider makes auth state available to all components
    <AuthProvider>
      {/* BrowserRouter enables client-side routing */}
      <BrowserRouter>
        {/* Routes defines all the pages in your app */}
        <Routes>
          {/* Root path - redirect to login */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          
          {/* Login page - anyone can access */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* Dashboard - protected route (must be logged in) */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            } 
          />

          {/* 404 - Catch all other routes */}
          <Route 
            path="*" 
            element={
              <div style={{ textAlign: 'center', marginTop: '50px' }}>
                <h1>404 - Page Not Found</h1>
                <p>The page you're looking for doesn't exist.</p>
              </div>
            } 
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
