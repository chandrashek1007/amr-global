import React, { useState } from 'react';
import { useTheme } from '../ThemeProvider'; // Import your custom theme hook
import { FaUserCircle } from 'react-icons/fa'; // User icon from react-icons
import { useNavigate } from 'react-router-dom';
import './Navbar.css';

function Navbar({ username, onLogout })  {
  const { theme, toggleTheme } = useTheme(); // Access theme and toggle function
  const [isMenuOpen, setIsMenuOpen] = useState(false); // Manage dropdown menu state
  const navigate = useNavigate();

  const handleMenuClick = (option) => {
    console.log(`${option} clicked`); // Log menu option
    setIsMenuOpen(false); // Close the menu
  };

  return (
    <nav className="navbar">
      <div>
        <img src="/images/logo.svg" alt="App Logo" className="navbar-logo-img" />
      </div>
      <div className="navbar-user-section">
      <span className="navbar-greeting">Hi, {username}!</span>
        <FaUserCircle
          className="user-icon"
          onClick={() => setIsMenuOpen((prev) => !prev)} // Toggle menu visibility
        />
        {isMenuOpen && (
      <ul className="dropdown-menu">
        <div className="dropdown-arrow"></div>
        
        <li className="dropdown-item" onClick={() => console.log('About')}>
        <a href="https://www.thevcp.co.uk/" target="_blank" rel="noopener noreferrer" className="dropdown-link">
      About
    </a>
        </li>
        <li className="dropdown-item" onClick={() => {
                onLogout();
                navigate('/login');
              }}>
          Logout
        </li>
      </ul>
    )}
      </div>
    </nav>
  );
}

export default Navbar;
