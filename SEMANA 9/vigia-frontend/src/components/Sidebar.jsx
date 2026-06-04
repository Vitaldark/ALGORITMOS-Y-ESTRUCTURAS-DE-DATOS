// src/components/Sidebar.jsx
import React, { useState } from 'react'

const SEV_COLOR = {
  Critica: 'var(--critica)',
  Alta: 'var(--alta)',
  Media: 'var(--media)',
  Baja: 'var(--baja)',
}

const REGIONS = ['Todas', 'Madre de Dios', 'Puno', 'Cusco']
const SEVS    = ['Todas', 'Critica', 'Alta', 'Media', 'Baja']

export default function Sidebar({ alertas, loading, onFilter, onSelectAlerta, selectedAlerta, onDetectar }) {
  const [region, setRegion]     = useState('Todas')
  const [sev, setSev]           = useState('Todas')
  const [detecting, setDetecting] = useState(false)
  const [detectResult, setDetectResult] = useState(null)
  const [zonaInput, setZonaInput] = useState('')

  const handleFilter = (newRegion, newSev) => {
    const r = newRegion ?? region
    const s = newSev ?? sev
    setRegion(r); setSev(s)
    onFilter(r === 'Todas' ? null : r, s === 'Todas' ? null : s)
  }

  const handleDetectar = async () => {
    if (!zonaInput.trim()) return
    setDetecting(true); setDetectResult(null)
    try {
      const r = await onDetectar(zonaInput.trim())
      setDetectResult(r)
    } catch { setDetectResult({ error: true }) }
    finally { setDetecting(false) }
  }

  return (
    <aside style={{
      width: 'var(--sidebar-width)',
      background: 'var(--bg-panel)',
      borderRight: '1px solid var(--border)',
      display: 'flex',
      flexDirection: 'column',
      flexShrink: 0,
      overflow: 'hidden',
    }}>
      {/* ─── Filters ─── */}
      <div style={{ padding: '12px 14px', borderBottom: '1px solid var(--border)' }}>
        <SectionLabel>FILTROS DE ALERTA</SectionLabel>

        <div style={{ marginTop: 8 }}>
          <FilterLabel>REGIÓN</FilterLabel>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 4 }}>
            {REGIONS.map(r => (
              <Chip key={r} active={region === r} onClick={() => handleFilter(r, null)}>
                {r === 'Todas' ? 'TODAS' : r.split(' ').map(w => w[0]).join('')}
              </Chip>
            ))}
          </div>
        </div>

        <div style={{ marginTop: 8 }}>
          <FilterLabel>SEVERIDAD</FilterLabel>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 4 }}>
            {SEVS.map(s => (
              <Chip key={s} active={sev === s} color={s !== 'Todas' ? SEV_COLOR[s] : null}
                    onClick={() => handleFilter(null, s)}>
                {s === 'Todas' ? 'TODAS' : s.toUpperCase()}
              </Chip>
            ))}
          </div>
        </div>
      </div>

      {/* ─── Alert list ─── */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '10px 0' }}>
        <div style={{ padding: '0 14px 6px' }}>
          <SectionLabel>
            ALERTAS ACTIVAS
            <span style={{
              marginLeft: 6,
              fontFamily: 'var(--font-mono)', fontSize: 9,
              color: 'var(--accent-cyan)',
              background: 'var(--accent-cyan)18',
              padding: '1px 5px', borderRadius: 2,
            }}>
              {alertas.length}
            </span>
          </SectionLabel>
        </div>

        {loading ? (
          <SkeletonList />
        ) : alertas.length === 0 ? (
          <EmptyState />
        ) : (
          alertas.map(a => (
            <AlertCard
              key={a.properties.id}
              alerta={a}
              selected={selectedAlerta?.properties?.id === a.properties.id}
              onClick={() => onSelectAlerta(a)}
            />
          ))
        )}
      </div>

      {/* ─── Detect panel ─── */}
      <div style={{
        padding: '12px 14px',
        borderTop: '1px solid var(--border)',
        background: 'var(--bg-secondary)',
      }}>
        <SectionLabel>ANÁLISIS BAJO DEMANDA</SectionLabel>
        <div style={{ marginTop: 8, display: 'flex', gap: 6 }}>
          <input
            value={zonaInput}
            onChange={e => setZonaInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleDetectar()}
            placeholder="Nombre de zona..."
            style={{
              flex: 1, background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              color: 'var(--text-primary)',
              fontFamily: 'var(--font-mono)', fontSize: 11,
              padding: '6px 8px', borderRadius: 4, outline: 'none',
            }}
          />
          <button
            onClick={handleDetectar}
            disabled={detecting || !zonaInput.trim()}
            style={{
              padding: '6px 10px', borderRadius: 4, border: 'none',
              background: detecting ? 'var(--border)' : 'var(--accent-cyan)',
              color: detecting ? 'var(--text-muted)' : 'var(--bg-primary)',
              fontFamily: 'var(--font-mono)', fontSize: 10,
              fontWeight: 700, cursor: detecting ? 'not-allowed' : 'pointer',
              letterSpacing: 1, flexShrink: 0,
              transition: 'all 0.2s',
            }}
          >
            {detecting ? '...' : 'SCAN'}
          </button>
        </div>

        {detectResult && !detectResult.error && (
          <div style={{
            marginTop: 8, padding: '8px 10px',
            background: 'var(--bg-card)',
            border: '1px solid var(--accent-green)40',
            borderRadius: 4, animation: 'fadeIn 0.3s ease',
          }}>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 13, color: 'var(--accent-green)', fontWeight: 700 }}>
              ✓ DETECCIÓN COMPLETADA
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-secondary)', marginTop: 4 }}>
              Zona: <span style={{ color: 'var(--text-primary)' }}>{detectResult.zona}</span>
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-secondary)' }}>
              Área: <span style={{ color: 'var(--accent-orange)' }}>{detectResult.ha_detectadas?.toLocaleString()} ha</span>
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-secondary)' }}>
              Confianza: <span style={{ color: 'var(--accent-cyan)' }}>{(detectResult.confianza * 100).toFixed(1)}%</span>
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--text-muted)', marginTop: 2 }}>
              Modelo: {detectResult.modelo}
            </div>
          </div>
        )}
        {detectResult?.error && (
          <div style={{
            marginTop: 8, padding: '6px 10px',
            background: 'var(--critica)10',
            border: '1px solid var(--critica)40',
            borderRadius: 4, fontFamily: 'var(--font-mono)', fontSize: 10,
            color: 'var(--critica)',
          }}>
            ✗ ERROR — Backend desconectado
          </div>
        )}
      </div>
    </aside>
  )
}

function AlertCard({ alerta, selected, onClick }) {
  const p = alerta.properties
  const color = SEV_COLOR[p.severidad] || 'var(--text-muted)'
  return (
    <div
      onClick={onClick}
      style={{
        padding: '10px 14px',
        cursor: 'pointer',
        borderLeft: `3px solid ${selected ? color : 'transparent'}`,
        background: selected ? `${color}08` : 'transparent',
        transition: 'all 0.15s',
        borderBottom: '1px solid var(--border)22',
      }}
      onMouseEnter={e => { if (!selected) e.currentTarget.style.background = 'var(--bg-card)' }}
      onMouseLeave={e => { if (!selected) e.currentTarget.style.background = 'transparent' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div style={{
          fontFamily: 'var(--font-display)', fontSize: 14,
          fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.2,
        }}>
          {p.zona}
        </div>
        <SevBadge sev={p.severidad} color={color} />
      </div>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-muted)', marginTop: 3 }}>
        {p.region} · {p.tipo}
      </div>
      <div style={{ display: 'flex', gap: 10, marginTop: 5 }}>
        <MetaTag label="HA" value={p.ha?.toLocaleString()} color="var(--accent-orange)" />
        <MetaTag label="IA" value={`${(p.confianza * 100).toFixed(0)}%`} color="var(--accent-cyan)" />
        <MetaTag label="FECHA" value={p.fecha} color="var(--text-muted)" />
      </div>
      {p.anp && (
        <div style={{
          marginTop: 4, fontSize: 9, fontFamily: 'var(--font-mono)',
          color: 'var(--critica)', letterSpacing: 1,
        }}>
          ⚠ {p.anp}
        </div>
      )}
    </div>
  )
}

function MetaTag({ label, value, color }) {
  return (
    <div style={{ display: 'flex', gap: 3, alignItems: 'center' }}>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: 8, color: 'var(--text-muted)', letterSpacing: 1 }}>
        {label}
      </span>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color, fontWeight: 700 }}>
        {value}
      </span>
    </div>
  )
}

function SevBadge({ sev, color }) {
  return (
    <span style={{
      fontFamily: 'var(--font-mono)', fontSize: 8,
      color, background: `${color}18`,
      border: `1px solid ${color}40`,
      padding: '1px 5px', borderRadius: 2, letterSpacing: 1,
      flexShrink: 0, marginLeft: 6,
    }}>
      {sev?.toUpperCase()}
    </span>
  )
}

function Chip({ children, active, color, onClick }) {
  const c = color || 'var(--accent-cyan)'
  return (
    <button onClick={onClick} style={{
      fontFamily: 'var(--font-mono)', fontSize: 9, letterSpacing: 1,
      padding: '3px 7px', borderRadius: 3, cursor: 'pointer',
      background: active ? `${c}20` : 'var(--bg-card)',
      border: `1px solid ${active ? c : 'var(--border)'}`,
      color: active ? c : 'var(--text-muted)',
      transition: 'all 0.15s',
    }}>
      {children}
    </button>
  )
}

function FilterLabel({ children }) {
  return (
    <div style={{
      fontFamily: 'var(--font-mono)', fontSize: 9,
      color: 'var(--text-muted)', letterSpacing: 2,
    }}>
      {children}
    </div>
  )
}

function SectionLabel({ children }) {
  return (
    <div style={{
      fontFamily: 'var(--font-mono)', fontSize: 10,
      fontWeight: 700, color: 'var(--text-secondary)',
      letterSpacing: 2, display: 'flex', alignItems: 'center',
    }}>
      {children}
    </div>
  )
}

function SkeletonList() {
  return (
    <div style={{ padding: '0 14px', display: 'flex', flexDirection: 'column', gap: 8 }}>
      {[...Array(5)].map((_, i) => (
        <div key={i} style={{
          height: 72, borderRadius: 4,
          background: 'linear-gradient(90deg, var(--bg-card) 25%, var(--border) 50%, var(--bg-card) 75%)',
          backgroundSize: '400px 100%',
          animation: 'shimmer 1.4s infinite',
        }} />
      ))}
    </div>
  )
}

function EmptyState() {
  return (
    <div style={{
      padding: '24px 14px', textAlign: 'center',
      fontFamily: 'var(--font-mono)', fontSize: 11,
      color: 'var(--text-muted)',
    }}>
      <div style={{ fontSize: 24, marginBottom: 8 }}>◎</div>
      Sin alertas con estos filtros
    </div>
  )
}
