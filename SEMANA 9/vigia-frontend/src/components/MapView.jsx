// src/components/MapView.jsx
import React, { useEffect, useRef } from 'react'

const SEV_COLOR = {
  Critica: '#ff2d55',
  Alta:    '#ff8c00',
  Media:   '#f0c040',
  Baja:    '#00e896',
}

// We use Leaflet directly (not react-leaflet) for full control
export default function MapView({ alertas, selectedAlerta, onSelectAlerta }) {
  const containerRef = useRef(null)
  const mapRef       = useRef(null)
  const markersRef   = useRef([])

  // Initialize map once
  useEffect(() => {
    if (mapRef.current) return
    const L = window.L
    if (!L) return

    const map = L.map(containerRef.current, {
      center: [-12.8, -69.9],
      zoom: 7,
      zoomControl: true,
      attributionControl: true,
    })

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap | VIGÍA SATELITAL',
      maxZoom: 18,
    }).addTo(map)

    mapRef.current = map
    return () => { map.remove(); mapRef.current = null }
  }, [])

  // Update markers when alertas change
  useEffect(() => {
    const L = window.L
    const map = mapRef.current
    if (!L || !map) return

    // Clear old markers
    markersRef.current.forEach(m => m.remove())
    markersRef.current = []

    alertas.forEach(feature => {
      const [lng, lat] = feature.geometry.coordinates
      const p = feature.properties
      const color = SEV_COLOR[p.severidad] || '#7ab8d4'
      const size  = p.severidad === 'Critica' ? 18 : p.severidad === 'Alta' ? 14 : 11

      // Custom HTML icon
      const icon = L.divIcon({
        className: '',
        html: `
          <div style="position:relative;width:${size + 10}px;height:${size + 10}px">
            <div style="
              position:absolute;top:50%;left:50%;
              transform:translate(-50%,-50%);
              width:${size + 10}px;height:${size + 10}px;
              border-radius:50%;
              border:1.5px solid ${color};
              opacity:0.4;
              animation:pulse-ring 2s ease-out infinite;
            "></div>
            <div style="
              position:absolute;top:50%;left:50%;
              transform:translate(-50%,-50%);
              width:${size}px;height:${size}px;
              border-radius:50%;
              background:${color}33;
              border:2px solid ${color};
              display:flex;align-items:center;justify-content:center;
              font-size:7px;font-weight:bold;color:${color};
              font-family:monospace;
            ">${p.ha >= 1000 ? Math.round(p.ha / 100) / 10 + 'K' : p.ha}</div>
          </div>
        `,
        iconSize:   [size + 10, size + 10],
        iconAnchor: [(size + 10) / 2, (size + 10) / 2],
      })

      const marker = L.marker([lat, lng], { icon })

      marker.bindPopup(`
        <div style="
          background:#0d1f2d;border:1px solid #1a3a4a;
          color:#e0f4ff;font-family:monospace;font-size:11px;
          min-width:200px;padding:2px;
        ">
          <div style="
            font-family:'Rajdhani',sans-serif;font-size:16px;
            font-weight:700;color:${color};padding-bottom:6px;
            border-bottom:1px solid #1a3a4a;margin-bottom:8px;
          ">${p.zona}</div>
          <div style="color:#7ab8d4;margin-bottom:2px">${p.region} · ${p.tipo}</div>
          <div style="display:flex;gap:12px;margin-top:6px">
            <span><span style="color:#3d7a9a">HA </span><span style="color:#ff8c00;font-weight:700">${p.ha?.toLocaleString()}</span></span>
            <span><span style="color:#3d7a9a">IA </span><span style="color:#00d4ff;font-weight:700">${(p.confianza * 100).toFixed(1)}%</span></span>
          </div>
          ${p.satelite ? `<div style="color:#3d7a9a;margin-top:4px;font-size:9px">SAT: ${p.satelite}</div>` : ''}
          ${p.anp ? `<div style="color:#ff2d55;margin-top:4px;font-size:9px">⚠ ${p.anp}</div>` : ''}
          <div style="color:#3d7a9a;margin-top:4px;font-size:9px">${p.fecha}</div>
        </div>
      `, {
        className: 'vigia-popup',
        maxWidth: 260,
      })

      marker.on('click', () => onSelectAlerta(feature))
      marker.addTo(map)
      markersRef.current.push(marker)
    })
  }, [alertas, onSelectAlerta])

  // Pan to selected
  useEffect(() => {
    const map = mapRef.current
    if (!map || !selectedAlerta) return
    const [lng, lat] = selectedAlerta.geometry.coordinates
    map.flyTo([lat, lng], 10, { duration: 1.2 })
  }, [selectedAlerta])

  return (
    <div style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>
      {/* Scanline overlay */}
      <div style={{
        position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
        pointerEvents: 'none', zIndex: 500, overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', top: 0, left: 0, right: 0,
          height: 2,
          background: 'linear-gradient(transparent, var(--accent-cyan)30, transparent)',
          animation: 'scanline 6s linear infinite',
        }} />
      </div>

      {/* Corner decorations */}
      <CornerDeco pos="top-left" />
      <CornerDeco pos="top-right" />
      <CornerDeco pos="bottom-left" />
      <CornerDeco pos="bottom-right" />

      {/* Coordinate overlay (bottom right above attribution) */}
      <MapCoords />

      {/* Map container */}
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />

      {/* Custom popup styles injected */}
      <style>{`
        .vigia-popup .leaflet-popup-content-wrapper {
          background: #0d1f2d !important;
          border: 1px solid #1a3a4a !important;
          border-radius: 4px !important;
          box-shadow: 0 4px 24px rgba(0,212,255,0.15) !important;
          padding: 0 !important;
        }
        .vigia-popup .leaflet-popup-content {
          margin: 10px 12px !important;
        }
        .vigia-popup .leaflet-popup-tip-container .leaflet-popup-tip {
          background: #1a3a4a !important;
        }
        .vigia-popup .leaflet-popup-close-button {
          color: #7ab8d4 !important;
          font-size: 16px !important;
        }
      `}</style>
    </div>
  )
}

function CornerDeco({ pos }) {
  const styles = {
    'top-left':     { top: 12, left: 12 },
    'top-right':    { top: 12, right: 12 },
    'bottom-left':  { bottom: 30, left: 12 },
    'bottom-right': { bottom: 30, right: 12 },
  }
  const isLeft  = pos.includes('left')
  const isTop   = pos.includes('top')
  return (
    <div style={{
      position: 'absolute', zIndex: 600, pointerEvents: 'none',
      width: 20, height: 20, ...styles[pos],
    }}>
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        {isTop && isLeft  && <><line x1="0" y1="0" x2="12" y2="0" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/><line x1="0" y1="0" x2="0" y2="12" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/></>}
        {isTop && !isLeft && <><line x1="20" y1="0" x2="8" y2="0" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/><line x1="20" y1="0" x2="20" y2="12" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/></>}
        {!isTop && isLeft  && <><line x1="0" y1="20" x2="12" y2="20" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/><line x1="0" y1="20" x2="0" y2="8" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/></>}
        {!isTop && !isLeft && <><line x1="20" y1="20" x2="8" y2="20" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/><line x1="20" y1="20" x2="20" y2="8" stroke="var(--accent-cyan)" strokeWidth="1.5" strokeOpacity="0.5"/></>}
      </svg>
    </div>
  )
}

function MapCoords() {
  const [coords, setCoords] = React.useState({ lat: -12.800, lng: -69.900 })
  return (
    <div style={{
      position: 'absolute', bottom: 24, right: 60,
      zIndex: 600, pointerEvents: 'none',
      fontFamily: 'var(--font-mono)', fontSize: 9,
      color: 'var(--text-muted)', letterSpacing: 1,
    }}>
      {coords.lat.toFixed(4)}°S {Math.abs(coords.lng).toFixed(4)}°W
    </div>
  )
}
