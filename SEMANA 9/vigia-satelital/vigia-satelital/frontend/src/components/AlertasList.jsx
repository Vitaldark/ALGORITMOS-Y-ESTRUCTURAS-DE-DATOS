import { useState } from 'react'

const SEV_COLOR = { Critica: '#e24b4a', Alta: '#ef9f27', Media: '#378add' }

export default function AlertasList({ alertas, onSelect, selected }) {
  const features = alertas?.features || []

  if (!features.length)
    return <div style={{ color:'#8b949e', fontSize:'12px', padding:'1rem' }}>No hay alertas para los filtros seleccionados.</div>

  return (
    <div style={{ display:'flex', flexDirection:'column' }}>
      {features.map(f => {
        const p   = f.properties
        const sel = selected?.properties?.id === p.id
        const c   = SEV_COLOR[p.severidad] || '#888'
        return (
          <div
            key={p.id}
            onClick={() => onSelect(f)}
            style={{
              padding:'10px 14px', borderBottom:'0.5px solid #30363d',
              cursor:'pointer', display:'flex', gap:'10px', alignItems:'flex-start',
              background: sel ? 'rgba(29,158,117,0.1)' : 'transparent',
              borderLeft: sel ? '2px solid #1d9e75' : '2px solid transparent',
              transition:'background 0.12s',
            }}
          >
            <div style={{ width:'26px', height:'26px', borderRadius:'6px', background:`${c}22`, color:c, display:'flex', alignItems:'center', justifyContent:'center', fontSize:'13px', flexShrink:0 }}>
              ⚠
            </div>
            <div style={{ flex:1, minWidth:0 }}>
              <div style={{ fontSize:'12px', fontWeight:'500', color:'#f0f6fc', overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>
                {p.zona} — {p.region}
              </div>
              <div style={{ fontSize:'10px', color:'#8b949e', fontFamily:'monospace', marginTop:'2px' }}>
                {p.fecha} · {p.ha?.toLocaleString()} ha · Conf. {(p.confianza*100).toFixed(0)}%
              </div>
            </div>
            <span style={{ fontSize:'10px', fontFamily:'monospace', padding:'2px 6px', borderRadius:'99px', background:`${c}22`, color:c, flexShrink:0 }}>
              {p.severidad}
            </span>
          </div>
        )
      })}
    </div>
  )
}
