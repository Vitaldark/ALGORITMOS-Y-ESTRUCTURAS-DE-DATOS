# VIGÍA SATELITAL — Frontend React
> Persona B — Sistema de Monitoreo de Minería Ilegal en la Amazonía Peruana

## 🚀 Instalación y Arranque

```bash
# 1. Instalar dependencias
npm install

# 2. Iniciar servidor de desarrollo
npm run dev

# 3. Abrir en el navegador
# → http://localhost:5173
```

## ⚙️ Configuración del Backend

Edita el archivo **`.env`** antes de arrancar:

```env
# Si Persona A corre localmente:
VITE_API_URL=http://localhost:8000

# Si Persona A está en Google Colab con ngrok:
VITE_API_URL=https://xxxx-xxx.ngrok-free.app
```

> 💡 La URL ngrok la comparte Persona A. Cambia el `.env` y **reinicia** `npm run dev`.

---

## 🗂 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx        ← Barra superior con estadísticas en tiempo real
│   │   ├── Sidebar.jsx       ← Filtros, lista de alertas, panel de detección
│   │   ├── MapView.jsx       ← Mapa Leaflet con marcadores dinámicos
│   │   ├── ChartsPanel.jsx   ← Gráficas Recharts (barras, pie, confianza)
│   │   └── ErrorBanner.jsx   ← Banner de error si el backend no responde
│   ├── hooks/
│   │   └── useAPI.js         ← Hook centralizado para todos los fetch al backend
│   ├── App.jsx               ← Componente raíz, gestión de estado global
│   ├── main.jsx              ← Entry point React
│   └── index.css             ← Variables CSS globales y animaciones
├── .env                      ← URL del backend (Persona A)
├── index.html
├── package.json
└── vite.config.js
```

---

## 🗺 Endpoints del Backend que consume el frontend

| Endpoint | Método | Descripción |
|---|---|---|
| `/alertas` | GET | Lista GeoJSON de alertas (acepta `?region=` y `?severidad=`) |
| `/estadisticas` | GET | Totales globales para el header |
| `/detectar?zona=` | POST | Análisis bajo demanda de una zona |

---

## 🎨 Funcionalidades del Frontend

- **Mapa interactivo** con marcadores de pulso animados por severidad
- **Filtros** por región (Madre de Dios, Puno, Cusco) y severidad
- **Panel de análisis bajo demanda** — escribe una zona y pulsa SCAN
- **Gráficas en tiempo real** — hectáreas por región, distribución de severidad, confianza IA
- **Conexión resiliente** — muestra banner de error si el backend no responde, con botón reintentar
- **Diseño oscuro táctico** — tema satelital/radar optimizado para monitoreo

---

## 🐛 Troubleshooting

**El mapa aparece en gris:**
→ Espera 2-3 segundos; Leaflet carga desde CDN.

**"BACKEND DESCONECTADO":**
→ Verifica que Persona A haya ejecutado `uvicorn main:app --reload` o que la URL ngrok sea correcta en `.env`.

**Error CORS:**
→ El backend ya tiene CORS abierto (`allow_origins=["*"]`). Si persiste, verifica la URL en `.env`.

**npm install falla:**
→ Requiere Node.js ≥ 18. Verifica con `node -v`.
