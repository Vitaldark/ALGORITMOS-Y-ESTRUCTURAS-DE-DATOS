import { useEffect, useRef, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON, Popup, useMap } from 'react-leaflet'
import { getAlertaGeoJSON } from '../services/api'
import 'leaflet/dist/leaflet.css'

// Colores por severidad
const SEV_COLOR = { Critica: '#e24b4a', Alta: '#ef9f27', Media: '#378add' }

function AlertaMarker({ feature, onSelect }) {
  const sev   = feature.properties.severidad
  const color = SEV_COLOR[sev] || '#888'

  const style = () => ({
    color, fillColor: color, fillOpacity: 0.55, weight: 2, radius: 8,
  })

  return null // implementado via GeoJSON onEachFeature
}

export default function MapReal({ alertas, onAlertaClick }) {
  const geoJsonRef = useRef()

  const puntosEstilo = (feature) => ({
    radius:      feature.properties.ha > 1000 ? 12 : feature.properties.ha > 500 ? 9 : 7,
    fillColor:   SEV_COLOR[feature.properties.severidad] || '#888',
    color:       '#fff',
    weight:      1.5,
    opacity:     1,
    fillOpacity: 0.85,
  })

  const onEachFeature = (feature, layer) => {
    const p = feature.properties
    layer.bindTooltip(`<strong>${p.zona}</strong><br/>${p.ha?.toLocaleString()} ha · ${p.severidad}`, {
      permanent: false, direction: 'top', className: 'vigia-tooltip'
    })
    layer.on('click', () => onAlertaClick && onAlertaClick(feature))
  }

  return (
    <MapContainer
      center={[-13.0, -70.2]}
      zoom={7}
      style={{ height: '100%', width: '100%', borderRadius: '8px' }}
      attributionControl={true}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='© OpenStreetMap'
      />
      {alertas?.features?.length > 0 && (
        <GeoJSON
          key={JSON.stringify(alertas)}
          data={alertas}
          pointToLayer={(feature, latlng) => {
            const L = window.L || require('leaflet')
            return L.circleMarker(latlng, puntosEstilo(feature))
          }}
          onEachFeature={onEachFeature}
        />
      )}
    </MapContainer>
  )
}
