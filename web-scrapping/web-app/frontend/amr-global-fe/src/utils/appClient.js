import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000", // Replace with your backend API URL
  timeout: 10000, // Request timeout in milliseconds
});

export default apiClient;
