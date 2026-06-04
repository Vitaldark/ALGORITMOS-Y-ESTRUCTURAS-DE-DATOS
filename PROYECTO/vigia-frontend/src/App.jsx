// src/App.jsx
import React, { useState, useEffect } from 'react'
import Header      from './components/Header.jsx'
import Sidebar     from './components/Sidebar.jsx'
import MapView     from './components/MapView.jsx'
import ChartsPanel from './components/ChartsPanel.jsx'
import ErrorBanner from './components/ErrorBanner.jsx'
import { useAPI }  from './hooks/useAPI.js'

export default function App() {
  const { alertas, estadisticas, loading, error, lastUpdate, fetchData, detectar, BASE } = useAPI()
  const [selectedAlerta, setSelectedAlerta] = useState(null)

  // Load Leaflet from CDN dynamically (since it needs window.L)
  useEffect(() => {
    if (window.L) return
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.async = true
    document.head.appendChild(script)
  }, [])

  const handleFilter = (region, severidad) => {
    setSelectedAlerta(null)
    fetchData(region, severidad)
  }

  const handleSelectAlerta = (feature) => {
    setSelectedAlerta(feature)
  }

  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      height: '100vh', width: '100vw', overflow: 'hidden',
    }}>
      {/* Header */}
      <Header
        estadisticas={estadisticas}
        loading={loading}
        lastUpdate={lastUpdate}
        error={error}
      />

      {/* Main body */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden', position: 'relative' }}>
        {/* Error banner (floating) */}
        {error && (
          <ErrorBanner BASE={BASE} onRetry={() => fetchData()} />
        )}

        {/* Sidebar */}
        <Sidebar
          alertas={alertas}
          loading={loading}
          onFilter={handleFilter}
          onSelectAlerta={handleSelectAlerta}
          selectedAlerta={selectedAlerta}
          onDetectar={detectar}
        />

        {/* Map + charts column */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <MapView
            alertas={alertas}
            selectedAlerta={selectedAlerta}
            onSelectAlerta={handleSelectAlerta}
          />
          <ChartsPanel alertas={alertas} />
        </div>
      </div>
    </div>
  )
}
