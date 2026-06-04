import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const api  = axios.create({ baseURL: BASE, timeout: 15000 })

export const getAlertas = (params = {}) =>
  api.get('/alertas', { params }).then(r => r.data)

export const getAlertaGeoJSON = (id) =>
  api.get(`/alertas/${id}/geojson`).then(r => r.data)

export const getEstadisticas = () =>
  api.get('/estadisticas').then(r => r.data)

export const triggerDeteccion = (zona) =>
  api.post('/detectar', null, { params: { zona } }).then(r => r.data)
