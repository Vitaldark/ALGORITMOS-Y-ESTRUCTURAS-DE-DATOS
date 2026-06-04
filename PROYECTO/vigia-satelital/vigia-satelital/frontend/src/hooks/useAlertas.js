import { useState, useEffect, useCallback } from 'react'
import { getAlertas, getEstadisticas } from '../services/api'

export function useAlertas(filtros = {}) {
  const [alertas, setAlertas]   = useState({ type: 'FeatureCollection', features: [] })
  const [stats,   setStats]     = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error,   setError]     = useState(null)

  const cargar = useCallback(async () => {
    try {
      setLoading(true)
      const [data, estadisticas] = await Promise.all([
        getAlertas(filtros),
        getEstadisticas(),
      ])
      setAlertas(data)
      setStats(estadisticas)
      setError(null)
    } catch (e) {
      setError('No se pudo conectar con el backend. ¿Está corriendo el servidor?')
    } finally {
      setLoading(false)
    }
  }, [JSON.stringify(filtros)])

  useEffect(() => { cargar() }, [cargar])

  return { alertas, stats, loading, error, recargar: cargar }
}
