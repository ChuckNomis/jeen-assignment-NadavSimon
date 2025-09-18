import axios from 'axios';

// Base URL for your FastAPI server
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Send a message to the chat endpoint
export const sendMessage = async (query) => {
  try {
    const response = await api.post('/api/chat', { query });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    
    if (error.response) {
      // Server responded with error status
      throw new Error(`Server error: ${error.response.data.detail || error.response.statusText}`);
    } else if (error.request) {
      // Network error
      throw new Error('Network error: Unable to connect to the server. Make sure the server is running on http://localhost:8000');
    } else {
      // Other error
      throw new Error(`Error: ${error.message}`);
    }
  }
};

// Health check endpoint
export const checkHealth = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    throw new Error('Server is not available');
  }
};

export default api;
