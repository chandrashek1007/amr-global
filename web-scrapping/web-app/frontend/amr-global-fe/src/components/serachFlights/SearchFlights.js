import React, { useState } from 'react';
import axios from 'axios'; // Import axios for API calls
import './SearchFlights.css';
import { FaSearch } from "react-icons/fa";
import { GrClearOption } from "react-icons/gr";
import { BiSearchAlt } from "react-icons/bi";
import { BiChevronLeft, BiChevronRight } from "react-icons/bi";


function SearchFlights() {
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [departureDate, setDepartureDate] = useState('');
  const [arrivalDate, setArrivalDate] = useState('');
  const [departureTimeRange, setDepartureTimeRange] = useState('');
  const [arrivalTimeRange, setArrivalTimeRange] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state
  const [currentPage, setCurrentPage] = useState(1);
  const resultsPerPage = 1;

  const timeRanges = [
    { label: '12 AM - 6 AM', value: '0AM-6AM' },
    { label: '6 AM - 12 PM', value: '6AM-12PM' },
    { label: '12 PM - 6 PM', value: '12PM-18PM' },
    { label: '6 PM - 12 AM', value: '18PM-24AM' },
  ];

  const firstTableResults = Array.isArray(searchResults)
  ? searchResults
  : searchResults.departure || [];

const indexOfLastResult = currentPage * resultsPerPage;
const indexOfFirstResult = indexOfLastResult - resultsPerPage;
const currentResults = firstTableResults.slice(indexOfFirstResult, indexOfLastResult);


const totalPages = Math.ceil(firstTableResults.length / resultsPerPage);

const handleNextPage = () => {
  if (currentPage < totalPages) setCurrentPage(currentPage + 1);
};

const handlePreviousPage = () => {
  if (currentPage > 1) setCurrentPage(currentPage - 1);
};


const handleSearch = async () => {
// Check if required fields are provided
  if (!source || !destination || !departureDate || !departureTimeRange) {
    setError('"Source", "Destination", "Departure date", and "Departure time range".');
    return;
  }
  setLoading(true); // Show loader
  setError(null); // Clear previous errors

  // Dynamically build params object, excluding empty fields
  const params = {};
  if (source) params.departure_location = source;
  if (destination) params.arrival_location = destination;
  if (departureDate) params.departure_date = departureDate;
  if (arrivalDate) params.arrival_date = arrivalDate;
  if (departureTimeRange) params.departure_range = departureTimeRange;
  if (arrivalTimeRange) params.arrival_range = arrivalTimeRange;

  try {
    const response = await axios.get('http://localhost:8000/flights', { params });
    setSearchResults(response.data); // Update results with API response
    console.log(response.data);
  } catch (err) {
    setError(err.message || 'An error occurred while fetching flight data.');
  } finally {
    setLoading(false); // Hide loader
  }
};
const locations = [
  { code: "BHX", name: "Birmingham Airport" },
  { code: "SOF", name: "Sofia Airport" }
];


  const handleClear = () => {
    setSource('');
    setDestination('');
    setDepartureDate('');
    setArrivalDate('');
    setDepartureTimeRange('');
    setArrivalTimeRange('');
    setSearchResults([]);
    setError(null);
  };

  // // Divide searchResults into two sections if needed
  // const firstTableResults = searchResults.departure || [];
  // const secondTableResults = searchResults.arrival || [];

  return (
    <div className="flight-search-container">
      <div className='align-icon'>
      <FaSearch style={{ fontSize: '1.3rem' }} />

      <div className='typography'>
      Flight Search</div>
      </div>
      {/* <h1 className='align-icon'><FaSearch /> 
      Flight Search</h1> */}
      <div className="search-form">
      <div className="form-group">
    <label htmlFor="source">Source Location</label>
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
    <label htmlFor="destination">Destination Location</label>
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
          <label htmlFor="departure-date">Date of Departure</label>
          <input
            type="date"
            id="departure-date"
            value={departureDate}
            onChange={(e) => setDepartureDate(e.target.value)}
          />
        </div>
        {/* <div className="form-group">
          <label htmlFor="arrival-date">Date of Arrival</label>
          <input
            type="date"
            id="arrival-date"
            value={arrivalDate}
            onChange={(e) => setArrivalDate(e.target.value)}
          />
        </div> */}
        <div className="form-group">
          <label htmlFor="departure-time-range">Departure Time Range</label>
          <select
            id="departure-time-range"
            value={departureTimeRange}
            onChange={(e) => setDepartureTimeRange(e.target.value)}
          >
            <option value="" disabled>
              Select a time range
            </option>
            {timeRanges.map((range) => (
              <option key={range.value} value={range.value}>
                {range.label}
              </option>
            ))}
          </select>
        </div>
        {/* <div className="form-group">
          <label htmlFor="arrival-time-range">Arrival Time Range</label>
          <select
            id="arrival-time-range"
            value={arrivalTimeRange}
            onChange={(e) => setArrivalTimeRange(e.target.value)}
          >
            <option value="" disabled>
              Select a time range
            </option>
            {timeRanges.map((range) => (
              <option key={range.value} value={range.value}>
                {range.label}
              </option>
            ))}
          </select>
        </div> */}
        <div className="button-group">
          <button className="search-button" onClick={handleSearch} disabled={loading}>
          <div className='button-text'>{loading ? 'Searching...' : 'Search'}<BiSearchAlt  style={{ fontSize: '2rem' }}/></div>
          
          </button>
          <button className="clear-button" onClick={handleClear} disabled={loading}>
            <div className='button-text'>Clear<GrClearOption style={{ fontSize: '0.9rem' }}/></div>
          </button>
        </div>
      </div>

      <div className="results-container">
        <div className='h2-typography'>Search Results</div>
        
        {error && <div className="error"> Please provide all required fields : {error}</div>}
        <div className="tables-column-container">
          <div className="table-wrapper">
          
            <table className="results-table">
              <thead>
                <tr>
                  <th>Sl. No.</th>
                  <th>Source</th>
                  <th>Destination</th>
                  <th>Departure Date</th>
                  <th>Departure Time</th>
                  <th>Price(£)</th>
                  <th>Book Link</th>
                </tr>
              </thead>
              <tbody>
                {firstTableResults.length > 0 ? (
                  firstTableResults.map((result, index) => (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{result.start_location}</td>
                      <td>{result.end_location}</td>
                      <td>{result.departure_date_time.split("T")[0]}</td> {/* Date */}
                      <td>{result.departure_date_time.split("T")[1]}</td> {/* Time */}
                      <td>{result.price}</td>
                      <td>
                        <a href={result.url} target="_blank" rel="noopener noreferrer">
                          Book Now
                        </a>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="7">No results found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          {/* Pagination Controls */}
        <div className="pagination">
          <button className='search-button' onClick={handlePreviousPage} disabled={currentPage === 1}>
          <BiChevronLeft style={{ fontSize: '1.5rem' }}/>
          </button>
          <span>
            Page {currentPage} of {totalPages}
          </span>
          <button onClick={handleNextPage} disabled={currentPage === totalPages}>
          <BiChevronRight style={{ fontSize: '1.5rem' }}/>
          </button>
        </div>
        </div>
      </div>
    </div>
  );
}

export default SearchFlights;
