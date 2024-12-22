import React, { useState } from 'react';
import Sidebar from '../../components/sidebar/Sidebar';
import './FlightManagement.css';
import SearchFlights from '../../components/serachFlights/SearchFlights';
import RequestAlert from '../../components/requestAlert/RequestAlert';
import { Button, TextField, Table, TableBody, TableCell, TableHead, TableRow, Dialog, DialogActions, DialogContent, DialogTitle, Badge, Typography } from '@mui/material';
import { Search as SearchIcon, List as ListIcon, Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, Person as PersonIcon } from '@mui/icons-material';
import Footer from '../../components/footer/Footer';
import Navbar from '../../components/navbar/Navbar';

export default function FlightManagement() {
  const [activeTab, setActiveTab] = useState("search");
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [showRequestModal, setShowRequestModal] = useState(false);
  const [requests, setRequests] = useState([]);
  const [flights, setFlights] = useState([]);

  const handleSearchFlights = (e) => {
    e.preventDefault();
    // Sample flight data
    const sampleFlights = [
      {
        id: "FL001",
        from: "New York",
        to: "London",
        departure: "2024-01-20 10:00",
        arrival: "2024-01-20 22:00",
        price: "$500",
      },
      {
        id: "FL002",
        from: "London",
        to: "Paris",
        departure: "2024-01-20 14:00",
        arrival: "2024-01-20 15:30",
        price: "$200",
      },
    ];
    setFlights(sampleFlights);
    setShowSearchResults(true);
  };

  const handleSubmitRequest = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const newRequest = {
      id: `REQ${(requests.length + 1).toString().padStart(3, "0")}`,
      from: formData.get("from"),
      to: formData.get("to"),
      date: formData.get("date"),
      status: "Pending",
      details: formData.get("details"),
    };
    setRequests([...requests, newRequest]);
    setShowRequestModal(false);
  };

  const deleteRequest = (id) => {
    setRequests(requests.filter((request) => request.id !== id));
  };

  return (
    <div className="content">
  <div className="scrollable-content">
    <Sidebar /> 
  </div>
</div>

  );
}
