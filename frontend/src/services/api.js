import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// JWT 토큰 자동 삽입
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 401 에러 시 자동 로그아웃
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  signup: (data) => api.post('/api/auth/signup', data),
  login: (data) => api.post('/api/auth/login', data),
  getProfile: () => api.get('/api/auth/profile'),
};

// Market Data API
export const marketAPI = {
  getSummary: () => api.get('/api/market/summary'),
  getDetails: (symbol) => api.get(`/api/market/details/${symbol}`),
};

// AI Reports API
export const reportsAPI = {
  getLatest: () => api.get('/api/reports/latest'),
  getHistory: (days = 7) => api.get(`/api/reports/history?days=${days}`),
};

// Multi Agent API
export const multiAgentAPI = {
  trigger: () => api.post('/api/multi-agent/trigger'),
  getStatus: (runId) => api.get(`/api/multi-agent/status/${runId}`),
};

export default api;
