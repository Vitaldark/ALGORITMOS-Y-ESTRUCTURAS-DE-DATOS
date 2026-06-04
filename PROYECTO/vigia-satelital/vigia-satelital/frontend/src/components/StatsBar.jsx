export default function StatsBar({ stats, loading }) {
  if (loading) return <div style={S.bar}><span style={S.muted}>Cargando estadísticas...</span></div>
  if (!stats)  return null

  const kpis = [
    { label: 'Alertas activas', value: stats.total_alertas,               color: '#e24b4a' },
    { label: 'Ha afectadas',    value: stats.hectareas_totales?.toLocaleString(), color: '#ef9f27' },
    { label: 'Alertas críticas',value: stats.alertas_criticas,             color: '#e24b4a' },
    { label: 'Conf. promedio',  value: `${(stats.confianza_promedio*100).toFixed(0)}%`, color: '#1d9e75' },
  ]

  return (
    <div style={S.bar}>
      {kpis.map(k => (
        <div key={k.label} style={S.kpi}>
          <div style={{ ...S.val, color: k.color }}>{k.value}</div>
          <div style={S.lbl}>{k.label}</div>
        </div>
      ))}
    </div>
  )
}

const S = {
  bar:  { display:'flex', gap:'8px', marginBottom:'12px', flexWrap:'wrap' },
  kpi:  { background:'#161b22', border:'0.5px solid #30363d', borderRadius:'8px', padding:'10px 14px', flex:'1', minWidth:'110px' },
  val:  { fontSize:'20px', fontWeight:'700', fontFamily:'monospace', lineHeight:1 },
  lbl:  { fontSize:'10px', color:'#8b949e', marginTop:'4px', textTransform:'uppercase', letterSpacing:'0.06em' },
  muted:{ color:'#8b949e', fontSize:'12px' },
}
