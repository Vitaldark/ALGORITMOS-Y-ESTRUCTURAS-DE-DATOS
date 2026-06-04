// src/components/ChartsPanel.jsx
import React from 'react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts'

const SEV_COLOR = {
  Critica: '#ff2d55',
  Alta:    '#ff8c00',
  Media:   '#f0c040',
  Baja:    '#00e896',
}

export default function ChartsPanel({ alertas }) {
  if (!alertas || alertas.length === 0) return null

  // Aggregate by region
  const byRegion = {}
  const bySev    = {}
  alertas.forEach(({ properties: p }) => {
    byRegion[p.region] = (byRegion[p.region] || 0) + p.ha
    bySev[p.severidad]  = (bySev[p.severidad] || 0) + 1
  })

  const regionData = Object.entries(byRegion).map(([name, ha]) => ({ name: name.split(' ')[0], ha }))
  const sevData    = Object.entries(bySev).map(([name, value]) => ({ name, value }))

  const CustomTooltip = ({ active, payload, label }) => {
    if (!active || !payload?.length) return null
    return (
      <div style={{
        background: 'var(--bg-card)', border: '1px solid var(--border)',
        padding: '6px 10px', borderRadius: 4,
        fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-primary)',
      }}>
        <div style={{ color: 'var(--text-muted)' }}>{label || payload[0]?.name}</div>
        <div style={{ color: 'var(--accent-orange)', fontWeight: 700 }}>
          {payload[0]?.value?.toLocaleString()} {payload[0]?.name === 'ha' || label ? 'ha' : ''}
        </div>
      </div>
    )
  }

  return (
    <div style={{
      display: 'flex', gap: 0,
      borderTop: '1px solid var(--border)',
      background: 'var(--bg-panel)',
      height: 140, flexShrink: 0,
    }}>
      {/* Hectareas por región */}
      <div style={{ flex: 1, padding: '10px 14px', borderRight: '1px solid var(--border)' }}>
        <ChartLabel>HECTÁREAS POR REGIÓN</ChartLabel>
        <ResponsiveContainer width="100%" height={100}>
          <BarChart data={regionData} margin={{ top: 4, right: 0, left: -20, bottom: 0 }}>
            <XAxis dataKey="name" tick={{ fill: '#3d7a9a', fontSize: 9, fontFamily: 'Space Mono' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: '#3d7a9a', fontSize: 8, fontFamily: 'Space Mono' }} axisLine={false} tickLine={false}
              tickFormatter={v => v >= 1000 ? `${v/1000}K` : v} />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,212,255,0.05)' }} />
            <Bar dataKey="ha" radius={[2, 2, 0, 0]}>
              {regionData.map((_, i) => (
                <Cell key={i} fill={['#ff8c00', '#00d4ff', '#f0c040'][i % 3]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pie by severity */}
      <div style={{ width: 200, padding: '10px 14px', borderRight: '1px solid var(--border)' }}>
        <ChartLabel>DISTRIBUCIÓN SEVERIDAD</ChartLabel>
        <ResponsiveContainer width="100%" height={100}>
          <PieChart>
            <Pie data={sevData} cx="50%" cy="50%" innerRadius={24} outerRadius={38}
              dataKey="value" stroke="none">
              {sevData.map((entry, i) => (
                <Cell key={i} fill={SEV_COLOR[entry.name] || '#7ab8d4'} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: 8, fontFamily: 'Space Mono', color: '#7ab8d4' }}
              formatter={(v) => v.toUpperCase()}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Confidence histogram */}
      <div style={{ flex: 1, padding: '10px 14px' }}>
        <ChartLabel>CONFIANZA IA — U-NET + RESNET50</ChartLabel>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginTop: 8 }}>
          {alertas.slice(0, 5).map(({ properties: p }) => (
            <div key={p.id} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <div style={{
                fontFamily: 'var(--font-mono)', fontSize: 8, color: 'var(--text-muted)',
                width: 60, flexShrink: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
              }}>
                {p.zona}
              </div>
              <div style={{
                flex: 1, height: 6, background: 'var(--bg-card)',
                borderRadius: 3, overflow: 'hidden',
              }}>
                <div style={{
                  height: '100%',
                  width: `${p.confianza * 100}%`,
                  background: `linear-gradient(90deg, var(--accent-cyan), var(--accent-green))`,
                  borderRadius: 3, transition: 'width 0.8s ease',
                }} />
              </div>
              <div style={{
                fontFamily: 'var(--font-mono)', fontSize: 8,
                color: 'var(--accent-cyan)', width: 32, textAlign: 'right', flexShrink: 0,
              }}>
                {(p.confianza * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function ChartLabel({ children }) {
  return (
    <div style={{
      fontFamily: 'var(--font-mono)', fontSize: 9,
      color: 'var(--text-muted)', letterSpacing: 2, marginBottom: 2,
    }}>
      {children}
    </div>
  )
}
