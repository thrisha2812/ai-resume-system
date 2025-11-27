import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import InterviewPage from './pages/InterviewPage';

// Simple protected route component
function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 font-sans">
        <Routes>
          <Route path="/" element={<LoginPage />} />
          
          <Route 
            path="/dashboard" 
            element={
              // We keep Dashboard protected so it redirects to login if "logged out",
              // but since we aren't using real auth, you can just login with dummy data.
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* --- FIX: REMOVED ProtectedRoute from here --- */}
          <Route path="/interview/:id" element={<InterviewPage />} />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;