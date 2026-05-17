// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:9000/api';

console.log('🔌 API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minutes (for large responses)
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`📤 ${config.method.toUpperCase()} ${config.url}`);
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
    console.log(`✅ ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    const status = error.response?.status;
    const message = error.response?.data?.detail || error.message;
    console.error(`❌ ${status}: ${message}`);
    return Promise.reject(error);
  }
);

export const runLLMPipeline = async (query) => {
  const response = await api.post('/pipeline/llm', { query });
  return response.data;
};

export const runRAGPipeline = async (query) => {
  const response = await api.post('/pipeline/rag', { query });
  return response.data;
};

export const runTigerGraphPipeline = async (query) => {
  const response = await api.post('/pipeline/tigergraph', { query });
  return response.data;
};

export const runAllPipelines = async (query) => {
  const response = await api.post('/pipelines/all', { query });
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;