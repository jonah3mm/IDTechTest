import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// --- Assets ---

export const getAssets = (params = {}) => {
  const query = new URLSearchParams()
  if (params.search) query.set('search', params.search)
  if (params.page) query.set('page', params.page)
  // NOTE: 'type' and 'status' filters are intentionally NOT wired up here yet.
  // The backend already supports them — see Feature 3 in the README.
  return api.get(`/assets?${query}`).then((r) => r.data)
}

export const getAsset = (id) => api.get(`/assets/${id}`).then((r) => r.data)

export const createAsset = (data) => api.post('/assets', data).then((r) => r.data)

export const updateAsset = (id, data) =>
  api.put(`/assets/${id}`, data).then((r) => r.data)

export const toggleAsset = (id) =>
  api.post(`/assets/${id}/toggle`).then((r) => r.data)

export const decommissionAsset = (id) =>
  api.post(`/assets/${id}/decommission`).then((r) => r.data)

export const deleteAsset = (id) => api.delete(`/assets/${id}`).then((r) => r.data)

// --- Clients ---

export const getClients = () => api.get('/clients').then((r) => r.data)

export const getClient = (id) => api.get(`/clients/${id}`).then((r) => r.data)

export const createClient = (data) => api.post('/clients', data).then((r) => r.data)

export const deleteClient = (id) => api.delete(`/clients/${id}`).then((r) => r.data)

export default api
