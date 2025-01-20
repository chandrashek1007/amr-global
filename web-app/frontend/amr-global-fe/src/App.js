import React, { useState } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/navbar/Navbar';
import Footer from './components/footer/Footer';
import Login from './pages/login/Login';
import FlightManagement from './pages/flightManagement/FlightManagement';
import { ThemeProvider } from './components/ThemeProvider';
import ProtectedRoute from './components/protectRoute/ProtectedRoute';
import Signup from './pages/signUp/Signup';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Authentication state
  const [username, setUsername] = useState('');
  const location = useLocation();

  // Pass a function to Login to update authentication status
  const handleLogin = (name) => {setIsAuthenticated(true); setUsername(name);};
  const handleLogout = () => {
    setIsAuthenticated(false);
    setUsername('');
  };
  return (
    <ThemeProvider>
      {location.pathname !== '/login' && location.pathname !== '/signup' && location.pathname !== '/' && <Navbar username={username} onLogout={handleLogout} />}
      <Routes>
        {/* Public Route */}
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/" element={<Signup />} />
        <Route path="/signup" element={<Signup />} />
        {/* Protected Route */}
        <Route
          path="/flights"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <FlightManagement />
            </ProtectedRoute>
          }
        />
      </Routes>
      <Footer />
    </ThemeProvider>
  );
}

export default App;