
import React, { useState } from 'react';
import './Sidebar.css';
import RequestAlert from '../requestAlert/RequestAlert';
import SearchFlights from '../serachFlights/SearchFlights';

function Sidebar() {
  const [activeTab, setActiveTab] = useState('search-flights');

  const renderActiveComponent = () => {
    if (activeTab === 'search-flights') return <SearchFlights />;
    if (activeTab === 'request-alerts') return <RequestAlert />;
    return null;
  };

  return (
    <div className="sidebar-container">
      {/* Sidebar */}
      <div className="sidebar">
        <button
          onClick={() => setActiveTab('search-flights')}
          className={`sidebar-tab ${activeTab === 'search-flights' ? 'active' : ''}`}
        >
          Search Flights
        </button>
        <button
          onClick={() => setActiveTab('request-alerts')}
          className={`sidebar-tab ${activeTab === 'request-alerts' ? 'active' : ''}`}
        >
          Request Alerts
        </button>
       
      </div>

      {/* Main Content */}
      <div className="sidebar-content">{renderActiveComponent()}</div>
    </div>
  );
}

export default Sidebar;
