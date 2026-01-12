/**
 * API Configuration
 * Axios instance with base URL and interceptors
 */
import axios from 'axios';

// API Base URL - change this for production
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30 seconds
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        // Add authentication token if available
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Log request in development
        if (import.meta.env.DEV) {
            console.log('🚀 API Request:', config.method?.toUpperCase(), config.url);
        }

        return config;
    },
    (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => {
        // Log response in development
        if (import.meta.env.DEV) {
            console.log('✅ API Response:', response.config.url, response.status);
        }

        return response.data;
    },
    (error) => {
        // Handle errors
        let message = error.message || 'An error occurred';

        // Handle FastAPI validation errors (422)
        if (error.response?.data?.detail) {
            const detail = error.response.data.detail;

            // If detail is an array of validation errors
            if (Array.isArray(detail)) {
                message = detail.map(err => {
                    const field = err.loc?.join('.') || 'unknown field';
                    return `${field}: ${err.msg}`;
                }).join(', ');
            } else if (typeof detail === 'string') {
                message = detail;
            } else {
                message = JSON.stringify(detail);
            }
        }

        console.error('❌ API Error:', {
            url: error.config?.url,
            status: error.response?.status,
            message,
            fullError: error.response?.data
        });

        // Handle specific error codes
        if (error.response?.status === 401) {
            // Unauthorized - redirect to login
            localStorage.removeItem('authToken');
            // window.location.href = '/login';
        }

        return Promise.reject(new Error(message));
    }
);

export default api;
