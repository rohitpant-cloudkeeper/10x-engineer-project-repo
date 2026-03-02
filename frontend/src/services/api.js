import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Prompts API
export const promptsAPI = {
  getAll: (params) => api.get('/prompts', { params }),
  getById: (id) => api.get(`/prompts/${id}`),
  create: (data) => api.post('/prompts', data),
  update: (id, data) => api.put(`/prompts/${id}`, data),
  patch: (id, data) => api.patch(`/prompts/${id}`, data),
  delete: (id) => api.delete(`/prompts/${id}`),
};

// Collections API
export const collectionsAPI = {
  getAll: () => api.get('/collections'),
  getById: (id) => api.get(`/collections/${id}`),
  create: (data) => api.post('/collections', data),
  delete: (id) => api.delete(`/collections/${id}`),
};

// Tags API
export const tagsAPI = {
  getAll: () => api.get('/tags'),
  getById: (name) => api.get(`/tags/${name}`),
  getPopular: (limit) => api.get('/tags/popular', { params: { limit } }),
};

// Versions API
export const versionsAPI = {
  getAll: (promptId, params) => api.get(`/prompts/${promptId}/versions`, { params }),
  getById: (promptId, version) => api.get(`/prompts/${promptId}/versions/${version}`),
  revert: (promptId, version) => api.post(`/prompts/${promptId}/versions/${version}/revert`),
  compare: (promptId, v1, v2) => api.get(`/prompts/${promptId}/versions/compare`, { params: { v1, v2 } }),
};

export default api;
