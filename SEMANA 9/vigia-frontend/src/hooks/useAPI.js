// src/hooks/useAPI.js
import { useState, useEffect, useCallback } from 'react'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function useAPI() {
  const [alertas, setAlertas] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)

  const fetchData = useCallback(async (region = null, severidad = null) => {
    setLoading(true)
    setError(null)
    try {
      // Build query params
      const params = new URLSearchParams()
      if (region)    params.append('region', region)
      if (severidad) params.append('severidad', severidad)

      const headers = { 'ngrok-skip-browser-warning': 'true' }

      const [alertasRes, statsRes] = await Promise.all([
        fetch(`${BASE}/alertas?${params}`, { headers }),
        fetch(`${BASE}/estadisticas`, { headers }),
      ])

      if (!alertasRes.ok || !statsRes.ok) throw new Error('Error del servidor')

      const alertasData = await alertasRes.json()
      const statsData   = await statsRes.json()

      setAlertas(alertasData.features || [])
      setEstadisticas(statsData)
      setLastUpdate(new Date())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  const detectar = useCallback(async (zona) => {
    const headers = {
      'Content-Type': 'application/json',
      'ngrok-skip-browser-warning': 'true',
    }
    const res = await fetch(`${BASE}/detectar?zona=${encodeURIComponent(zona)}`, {
      method: 'POST',
      headers,
    })
    if (!res.ok) throw new Error('Error en detección')
    return res.json()
  }, [])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return { alertas, estadisticas, loading, error, lastUpdate, fetchData, detectar, BASE }
}
