import { useState, lazy, Suspense } from 'react'
import { useAlertas } from './hooks/useAlertas'
import StatsBar from './components/StatsBar'
import AlertasList from './components/AlertasList'
import { triggerDeteccion } from './services/api'

const MapReal = lazy(() => import('./components/MapReal'))

export default function App() {
  const [filtros,   setFiltros]   = useState({})
  const [selected,  setSelected]  = useState(null)
  const [simState,  setSimState]  = useState(null)

  const { alertas, stats, loading, error, recargar } = useAlertas(filtros)

  const handleDetectar = async (zona) => {
    setSimState({ estado: 'ejecutando', zona })
    try {
      const res = await triggerDeteccion(zona)
      setSimState({ estado: 'ok', ...res })
      recargar()
    } catch {
      setSimState({ estado: 'error', zona })
    }
  }

  return (
    <div style={S.app}>
      {/* Header */}
      <div style={S.header}>
        <div style={S.brand}>
          <div style={S.brandIcon}>🛰</div>
          <div>
            <div style={S.brandName}>VIGÍA SATELITAL</div>
            <div style={S.brandSub}>v1.0 · Perú · CRISP-DM + CNN · SIS210</div>
          </div>
        </div>
        <div style={S.headerRight}>
          <div style={S.statusPill}>
            <div style={S.pulse}></div>
            <span style={{ color:'#1d9e75' }}>API CONECTADA</span>
          </div>
        </div>
      </div>

      {/* Error banner */}
      {error && (
        <div style={S.errorBanner}>
          ⚠ {error}
          <span style={{ marginLeft:'8px', fontSize:'11px', opacity:0.7 }}>
            Iniciar backend: <code>cd backend && uvicorn main:app --reload</code>
          </span>
        </div>
      )}

      {/* KPIs */}
      <div style={S.content}>
        <StatsBar stats={stats} loading={loading} />

        {/* Filtros */}
        <div style={S.filterRow}>
          {['Madre de Dios','Puno','Cusco'].map(r => (
            <button key={r} onClick={() => setFiltros(f => f.region === r ? {} : {...f, region: r})}
              style={{ ...S.fbtn, ...(filtros.region === r ? S.fbtnActive : {}) }}>
              {r}
            </button>
          ))}
          {['Critica','Alta','Media'].map(s => (
            <button key={s} onClick={() => setFiltros(f => f.severidad === s ? {} : {...f, severidad: s})}
              style={{ ...S.fbtn, ...(filtros.severidad === s ? S.fbtnActive : {}) }}>
              {s}
            </button>
          ))}
          <button onClick={() => setFiltros({})} style={S.fbtn}>Limpiar</button>
          <button onClick={recargar} style={{ ...S.fbtn, marginLeft:'auto' }}>↻ Actualizar</button>
        </div>

        {/* Layout principal */}
        <div style={S.main}>
          {/* Mapa */}
          <div style={S.mapBox}>
            <Suspense fallback={<div style={S.mapPlaceholder}>Cargando mapa...</div>}>
              <MapReal alertas={alertas} onAlertaClick={setSelected} />
            </Suspense>
          </div>

          {/* Panel lateral */}
          <div style={S.sidebar}>
            {/* Detalle alerta seleccionada */}
            {selected && (
              <div style={S.detailCard}>
                <div style={S.detailHeader}>
                  <div style={S.detailTitle}>{selected.properties.zona}</div>
                  <span style={{ ...S.sevTag, background:`${SEV_COLOR[selected.properties.severidad]}22`, color:SEV_COLOR[selected.properties.severidad] }}>
                    {selected.properties.severidad}
                  </span>
                </div>
                <div style={S.detailSub}>{selected.properties.region} · {selected.properties.fecha}</div>
                <div style={S.detailGrid}>
                  {[
                    ['Área',     `${selected.properties.ha?.toLocaleString()} ha`],
                    ['Confianza',`${(selected.properties.confianza*100).toFixed(0)}%`],
                    ['Tipo',      selected.properties.tipo],
                    ['Satélite', 'Sentinel-2'],
                  ].map(([k,v]) => (
                    <div key={k} style={S.field}><div style={S.fieldL}>{k}</div><div style={S.fieldV}>{v}</div></div>
                  ))}
                </div>
                <button style={S.btnPrimary} onClick={() => handleDetectar(selected.properties.zona)}>
                  ▶ Ejecutar detección en esta zona
                </button>
              </div>
            )}

            {/* Simulación result */}
            {simState && (
              <div style={{ ...S.detailCard, borderColor: simState.estado==='ok'?'rgba(29,158,117,.4)':'rgba(226,75,74,.4)' }}>
                {simState.estado === 'ejecutando' && <div style={{ color:'#378add', fontSize:'12px', fontFamily:'monospace' }}>Ejecutando pipeline de detección en {simState.zona}...</div>}
                {simState.estado === 'ok' && (
                  <>
                    <div style={{ color:'#1d9e75', fontSize:'12px', fontFamily:'monospace', marginBottom:'6px' }}>✓ Detección completada</div>
                    <div style={{ fontSize:'11px', color:'#8b949e', fontFamily:'monospace', lineHeight:1.7 }}>
                      Zona: {simState.zona}<br/>
                      Área detectada: {simState.ha_detectadas?.toLocaleString()} ha<br/>
                      Confianza: {(simState.confianza*100).toFixed(0)}%<br/>
                      Modelo: {simState.modelo}
                    </div>
                  </>
                )}
                {simState.estado === 'error' && <div style={{ color:'#e24b4a', fontSize:'12px', fontFamily:'monospace' }}>✗ Error en la detección</div>}
              </div>
            )}

            {/* Lista de alertas */}
            <div style={S.listPanel}>
              <div style={S.listHeader}>
                Feed de alertas
                <span style={{ color:'#8b949e', fontSize:'10px' }}>{alertas?.total} registros</span>
              </div>
              <AlertasList alertas={alertas} onSelect={setSelected} selected={selected} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const SEV_COLOR = { Critica: '#e24b4a', Alta: '#ef9f27', Media: '#378add' }

const S = {
  app:         { background:'#0d1117', color:'#c9d1d9', minHeight:'100vh', fontFamily:"'Segoe UI', sans-serif", fontSize:'13px' },
  header:      { background:'#161b22', borderBottom:'0.5px solid #30363d', padding:'9px 16px', display:'flex', alignItems:'center', justifyContent:'space-between' },
  brand:       { display:'flex', alignItems:'center', gap:'9px' },
  brandIcon:   { width:'26px', height:'26px', background:'#1d9e75', borderRadius:'5px', display:'flex', alignItems:'center', justifyContent:'center', fontSize:'14px' },
  brandName:   { fontSize:'13px', fontWeight:'700', color:'#f0f6fc', letterSpacing:'0.04em' },
  brandSub:    { fontSize:'10px', color:'#8b949e', fontFamily:'monospace' },
  headerRight: { display:'flex', alignItems:'center', gap:'12px' },
  statusPill:  { display:'flex', alignItems:'center', gap:'5px', fontSize:'11px', fontFamily:'monospace' },
  pulse:       { width:'6px', height:'6px', borderRadius:'50%', background:'#1d9e75', animation:'none' },
  errorBanner: { background:'rgba(226,75,74,0.1)', borderBottom:'1px solid rgba(226,75,74,0.3)', padding:'8px 16px', fontSize:'12px', color:'#e24b4a' },
  content:     { padding:'12px 14px' },
  filterRow:   { display:'flex', gap:'6px', marginBottom:'10px', flexWrap:'wrap', alignItems:'center' },
  fbtn:        { background:'transparent', border:'0.5px solid #30363d', borderRadius:'6px', padding:'5px 10px', fontSize:'11px', fontFamily:'monospace', color:'#8b949e', cursor:'pointer' },
  fbtnActive:  { background:'rgba(29,158,117,0.1)', borderColor:'rgba(29,158,117,0.4)', color:'#1d9e75' },
  main:        { display:'grid', gridTemplateColumns:'1fr 300px', gap:'10px', height:'calc(100vh - 170px)', minHeight:'400px' },
  mapBox:      { background:'#161b22', borderRadius:'10px', border:'0.5px solid #30363d', overflow:'hidden' },
  mapPlaceholder:{ display:'flex', alignItems:'center', justifyContent:'center', height:'100%', color:'#8b949e', fontSize:'12px' },
  sidebar:     { display:'flex', flexDirection:'column', gap:'8px', overflow:'auto' },
  detailCard:  { background:'#161b22', border:'0.5px solid rgba(29,158,117,0.35)', borderRadius:'10px', padding:'12px 14px' },
  detailHeader:{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:'3px' },
  detailTitle: { fontSize:'13px', fontWeight:'500', color:'#f0f6fc' },
  detailSub:   { fontSize:'10px', color:'#8b949e', fontFamily:'monospace', marginBottom:'9px' },
  detailGrid:  { display:'grid', gridTemplateColumns:'1fr 1fr', gap:'6px', marginBottom:'9px' },
  field:       { background:'#0d1117', borderRadius:'6px', padding:'6px 8px' },
  fieldL:      { fontSize:'9px', color:'#8b949e', fontFamily:'monospace', textTransform:'uppercase', letterSpacing:'0.06em', marginBottom:'2px' },
  fieldV:      { fontSize:'12px', color:'#f0f6fc', fontWeight:'500', fontFamily:'monospace' },
  sevTag:      { fontSize:'10px', fontFamily:'monospace', padding:'2px 7px', borderRadius:'99px' },
  btnPrimary:  { background:'#1d9e75', color:'#fff', border:'none', borderRadius:'6px', padding:'7px 12px', fontSize:'11px', cursor:'pointer', width:'100%', fontWeight:'500' },
  listPanel:   { background:'#161b22', border:'0.5px solid #30363d', borderRadius:'10px', overflow:'hidden', flex:1 },
  listHeader:  { padding:'9px 13px', borderBottom:'0.5px solid #30363d', fontSize:'11px', fontWeight:'500', color:'#f0f6fc', fontFamily:'monospace', textTransform:'uppercase', letterSpacing:'0.06em', display:'flex', justifyContent:'space-between', alignItems:'center' },
}
