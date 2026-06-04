// src/components/ErrorBanner.jsx
import React from 'react'

export default function ErrorBanner({ BASE, onRetry }) {
  return (
    <div style={{
      position: 'absolute', top: 12, left: '50%', transform: 'translateX(-50%)',
      zIndex: 2000, animation: 'fadeIn 0.3s ease',
      background: 'var(--bg-card)',
      border: '1px solid var(--critica)',
      borderRadius: 6, padding: '10px 16px',
      display: 'flex', alignItems: 'center', gap: 12,
      boxShadow: '0 4px 24px rgba(255,45,85,0.3)',
      maxWidth: '90vw',
    }}>
      <div style={{
        width: 8, height: 8, borderRadius: '50%',
        background: 'var(--critica)',
        animation: 'blink 1s ease-in-out infinite', flexShrink: 0,
      }} />
      <div>
        <div style={{
          fontFamily: 'var(--font-mono)', fontSize: 11,
          fontWeight: 700, color: 'var(--critica)', letterSpacing: 1,
        }}>
          BACKEND DESCONECTADO
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)', fontSize: 9,
          color: 'var(--text-muted)', marginTop: 2,
        }}>
          No se puede alcanzar <span style={{ color: 'var(--accent-cyan)' }}>{BASE}</span>
          {' '}· Verifica que Persona A haya iniciado el servidor
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)', fontSize: 9,
          color: 'var(--text-muted)', marginTop: 2,
        }}>
          Edita <code style={{ color: 'var(--accent-yellow)' }}>.env → VITE_API_URL</code> con tu URL ngrok si Persona A está en Colab
        </div>
      </div>
      <button onClick={onRetry} style={{
        fontFamily: 'var(--font-mono)', fontSize: 9, letterSpacing: 1,
        padding: '5px 10px', borderRadius: 3, cursor: 'pointer',
        background: 'var(--critica)20', border: '1px solid var(--critica)',
        color: 'var(--critica)', flexShrink: 0,
        transition: 'all 0.15s',
      }}
        onMouseEnter={e => e.target.style.background = 'var(--critica)40'}
        onMouseLeave={e => e.target.style.background = 'var(--critica)20'}
      >
        REINTENTAR
      </button>
    </div>
  )
}
