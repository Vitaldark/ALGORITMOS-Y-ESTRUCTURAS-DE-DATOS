// src/components/Header.jsx
import React from 'react'

const SEV_COLOR = {
  Critica: 'var(--critica)',
  Alta: 'var(--alta)',
  Media: 'var(--media)',
  Baja: 'var(--baja)',
}

export default function Header({ estadisticas, loading, lastUpdate, error }) {
  const fmt = (n) => n?.toLocaleString('es-PE') ?? '—'
  const timeStr = lastUpdate
    ? lastUpdate.toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : null

  return (
    <header style={{
      height: 'var(--header-height)',
      background: 'var(--bg-panel)',
      borderBottom: '1px solid var(--border)',
      display: 'flex',
      alignItems: 'center',
      padding: '0 16px',
      gap: 20,
      position: 'relative',
      zIndex: 1000,
      flexShrink: 0,
    }}>
      {/* Logo / Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
        <SatelliteIcon />
        <div>
          <div style={{
            fontFamily: 'var(--font-display)',
            fontSize: 18,
            fontWeight: 700,
            letterSpacing: 3,
            color: 'var(--accent-cyan)',
            lineHeight: 1,
          }}>
            VIGÍA SATELITAL
          </div>
          <div style={{
            fontFamily: 'var(--font-mono)',
            fontSize: 9,
            color: 'var(--text-muted)',
            letterSpacing: 2,
          }}>
            DETECCIÓN DE MINERÍA ILEGAL · AMAZONÍA PERUANA
          </div>
        </div>
      </div>

      <div style={{ width: 1, height: 30, background: 'var(--border)', flexShrink: 0 }} />

      {/* Stats pills */}
      {estadisticas && !error ? (
        <div style={{ display: 'flex', gap: 8, flex: 1, flexWrap: 'wrap' }}>
          <StatPill label="ALERTAS" value={fmt(estadisticas.total_alertas)} color="var(--accent-cyan)" />
          <StatPill label="CRÍTICAS" value={fmt(estadisticas.alertas_criticas)} color="var(--critica)" />
          <StatPill label="HECTÁREAS" value={fmt(estadisticas.hectareas_totales)} color="var(--accent-orange)" />
          <StatPill
            label="CONFIANZA IA"
            value={`${(estadisticas.confianza_promedio * 100).toFixed(1)}%`}
            color="var(--accent-green)"
          />
        </div>
      ) : (
        <div style={{ flex: 1 }} />
      )}

      {/* Status indicator */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
        {error ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div style={{
              width: 7, height: 7, borderRadius: '50%',
              background: 'var(--critica)',
              animation: 'blink 1s ease-in-out infinite',
            }} />
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--critica)' }}>
              BACKEND DESCONECTADO
            </span>
          </div>
        ) : loading ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div style={{
              width: 12, height: 12,
              border: '1.5px solid var(--border)',
              borderTopColor: 'var(--accent-cyan)',
              borderRadius: '50%',
              animation: 'spin 0.8s linear infinite',
            }} />
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-muted)' }}>
              SINCRONIZANDO...
            </span>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div style={{ width: 7, height: 7, borderRadius: '50%', background: 'var(--accent-green)' }} />
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-muted)' }}>
              {timeStr ? `ACTIVO · ${timeStr}` : 'ACTIVO'}
            </span>
          </div>
        )}
      </div>
    </header>
  )
}

function StatPill({ label, value, color }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      padding: '3px 12px',
      background: 'var(--bg-card)',
      border: `1px solid ${color}22`,
      borderRadius: 4,
    }}>
      <span style={{
        fontFamily: 'var(--font-mono)', fontSize: 8,
        color: 'var(--text-muted)', letterSpacing: 2,
      }}>{label}</span>
      <span style={{
        fontFamily: 'var(--font-display)', fontSize: 16,
        fontWeight: 700, color, lineHeight: 1.2,
      }}>{value}</span>
    </div>
  )
}

function SatelliteIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
      <circle cx="14" cy="14" r="13.5" stroke="var(--accent-cyan)" strokeWidth="0.5" strokeDasharray="3 2" />
      <circle cx="14" cy="14" r="4" fill="var(--accent-cyan)" fillOpacity="0.15" stroke="var(--accent-cyan)" strokeWidth="1" />
      <circle cx="14" cy="14" r="1.5" fill="var(--accent-cyan)" />
      <line x1="14" y1="10" x2="14" y2="4" stroke="var(--accent-cyan)" strokeWidth="1" strokeOpacity="0.6" />
      <line x1="14" y1="18" x2="14" y2="24" stroke="var(--accent-cyan)" strokeWidth="1" strokeOpacity="0.6" />
      <line x1="10" y1="14" x2="4" y2="14" stroke="var(--accent-cyan)" strokeWidth="1" strokeOpacity="0.6" />
      <line x1="18" y1="14" x2="24" y2="14" stroke="var(--accent-cyan)" strokeWidth="1" strokeOpacity="0.6" />
      <rect x="5" y="12.5" width="3" height="3" rx="0.5" fill="var(--accent-cyan)" fillOpacity="0.5" />
      <rect x="20" y="12.5" width="3" height="3" rx="0.5" fill="var(--accent-cyan)" fillOpacity="0.5" />
    </svg>
  )
}
