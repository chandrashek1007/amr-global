import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RequestAlert.css';
import { MdNotificationsActive } from "react-icons/md";
import { MdAddCircleOutline } from "react-icons/md";
import { FaEdit } from "react-icons/fa";
import { MdDelete } from "react-icons/md";

const RequestAlert = () => {
  const [alerts, setAlerts] = useState([]); // State to store alerts
  const [showModal, setShowModal] = useState(false); // Modal visibility
  const [editAlertId, setEditAlertId] = useState(null); // Track the alert being edited
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [departureDate, setDepartureDate] = useState('');
  const [departureTimeRange, setDepartureTimeRange] = useState('');
  const [estimatedPrice, setEstimatedPrice] = useState('');
  const [tillDate, setTillDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const timeRanges = [
    { label: '12 AM - 6 AM', value: '0AM-6AM' },
    { label: '6 AM - 12 PM', value: '6AM-12PM' },
    { label: '12 PM - 6 PM', value: '12PM-18PM' },
    { label: '6 PM - 12 AM', value: '18PM-24AM' },
  ];

  // Fetch alerts from the API
  const fetchAlerts = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.get('http://localhost:8000/notifications/?user_id=1');
      setAlerts(response.data.notifications || []);
    } catch (err) {
      setError('Failed to fetch alerts. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleAddOrUpdateAlert = async () => {
    if (!source || !destination || !departureDate || !departureTimeRange || !estimatedPrice || !tillDate) {
      alert('Please fill in all fields before saving.');
      return;
    }
  
    const alertData = {
      source,
      destination,
      departure_date: departureDate,
      departure_time_range: departureTimeRange,
      estimated_price: parseFloat(estimatedPrice),
      track_till_date: tillDate,
      user_id: 1, // Example user ID
    };
  
    try {
      setLoading(true);
      setError('');
  
      if (editAlertId) {
        // Update existing alert
        await axios.put(`http://localhost:8000/notifications/${editAlertId}`, alertData);
        setAlerts((prevAlerts) =>
          prevAlerts.map((alert) =>
            alert.id === editAlertId ? { ...alert, ...alertData } : alert
          )
        );
      } else {
        // Add new alert
        const response = await axios.post('http://localhost:8000/notifications/', alertData);
        setAlerts((prevAlerts) => [...prevAlerts, response.data.notification]);
      }
  
      // Reset form and modal
      resetForm();
      setShowModal(false);
    } catch {
      setError('Failed to save the alert. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const openEditModal = (alert) => {
    setEditAlertId(alert.id); // Set the alert ID for editing
    setSource(alert.source);
    setDestination(alert.destination);
    setDepartureDate(alert.departure_date);
    setDepartureTimeRange(alert.departure_time_range);
    setEstimatedPrice(alert.estimated_price.toString());
    setTillDate(alert.track_till_date);
    setShowModal(true); // Show modal
  };
  
  const openAddModal = () => {
    resetForm(); // Clear form state
    setShowModal(true); // Show modal for adding
  };
  const handleDeleteAlert = async (id) => {
    try {
      setLoading(true);
      setError('');
      await axios.delete(`http://localhost:8000/notifications/${id}`);
      fetchAlerts(); // Refresh alerts
    } catch (err) {
      setError('Failed to delete the alert. Please try again.');
    } finally {
      setLoading(false);
    }
  };



  const resetForm = () => {
    setSource('');
    setDestination('');
    setDepartureDate('');
    setDepartureTimeRange('');
    setEstimatedPrice('');
    setTillDate('');
    setEditAlertId(null);
  };

  const locations = [
    { code: "BHX", name: "Birmingham Airport" },
    { code: "SOF", name: "Sofia Airport" }
  ];

  return (
    <div className="request-alert-container">

      <div className='align-icon'>
      <MdNotificationsActive style={{ fontSize: '1.5rem' }}/>

      <div className='typography'>
      Request Alert</div>
      </div>

      {/* Add New Alert Button */}
      <button className="add-alert-button" onClick={openAddModal}>
     
      <MdAddCircleOutline style={{ fontSize: '1rem' }}/> 
      <div className='h2-typography-text'>Add New Alert</div>
 
      </button>

      {/* Modal for adding or updating alert */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
          <div className='modal-typography'>{editAlertId ? 'Update Alert' : 'Add New Alert'}</div>
           
            {error && <div className="error-message">{error}</div>}
            <div className="form-group">
              <label>Source</label>
              
              <select
                id="source"
                value={source}
                onChange={(e) => setSource(e.target.value)}
              >
                <option value="">Select Source Location</option> {/* Default placeholder */}
                {locations.map((location) => (
                  <option key={location.code} value={location.code}>
                    {location.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Destination</label>
              
               <select
                    id="destination"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                  >
                    <option value="">Select Destination Location</option> {/* Default placeholder */}
                    {locations
                      .filter((location) => location.code !== source) // Filter out selected source
                      .map((destination) => (
                        <option key={destination.code} value={destination.code}>
                          {destination.name}
                        </option>
                      ))}
                  </select>
            </div>
            <div className="form-group">
              <label>Departure Date</label>
              <input
                type="date"
                value={departureDate}
                onChange={(e) => setDepartureDate(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Track Till Date</label>
              <input
                type="date"
                value={tillDate}
                onChange={(e) => setTillDate(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Time Range</label>
              <select
                value={departureTimeRange}
                onChange={(e) => setDepartureTimeRange(e.target.value)}
              >
                <option value="" disabled>
                  Select Time Range
                </option>
                {timeRanges.map((range) => (
                  <option key={range.value} value={range.value}>
                    {range.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Expected Price (£)</label>
              <input
                type="number"
                value={estimatedPrice}
                onChange={(e) => setEstimatedPrice(e.target.value)}
                placeholder="Enter expected price"
              />
            </div>
            <div className="button-group">
              <button
                className="submit-button"
                onClick={handleAddOrUpdateAlert}
                disabled={loading}
              >
                {loading ? 'Saving...' : editAlertId ? 'Update Alert' : 'Add Alert'}
              </button>
              <button
                className="cancel-button"
                onClick={() => setShowModal(false)}
                disabled={loading}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Alerts Table */}
      <div className="alerts-table-container">
      <div className='h2-typography-text'>Added Alerts</div>
     
        {loading ? (
          <p className='p-typography-text'>Loading...</p>
        ) : error ? (
          <p className="error-message">{error}</p>
        ) : alerts.length === 0 ? (
          <p className='p-typography-text'>No Results Found</p>
        ) : (
          <table className="alerts-table">
            <thead>
              <tr>
                <th>Sl. No.</th>
                <th>Source</th>
                <th>Destination</th>
                <th>Departure Date</th>
                <th>Track Till Date</th>
                <th>Status</th>
                <th>Time Range</th>
                <th>Expected Price (£)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert, index) => (
                <tr key={alert.id}>
                  <td>{index + 1}</td>
                  <td>{alert.source}</td>
                  <td>{alert.destination}</td>
                  <td>{alert.departure_date}</td>
                  <td>{alert.track_till_date}</td>
                  <td>{alert.status}</td>
                  <td>
                    {
                      timeRanges.find(
                        (range) => range.value === alert.departure_time_range
                      )?.label
                    }
                  </td>
                  <td>£{alert.estimated_price.toFixed(2)}</td>
                  <td className="edit-delete-split">
                  <FaEdit  style={{ fontSize: '1rem' , 'color':'black' }} onClick={() => openEditModal(alert)}/>
                  <MdDelete style={{ fontSize: '1rem', 'color':'red'  }}  onClick={() => handleDeleteAlert(alert.id)}/>
                    
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default RequestAlert;
