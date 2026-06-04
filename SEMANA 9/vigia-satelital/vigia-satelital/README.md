# VIGÍA SATELITAL — Sistema de Detección de Minería Ilegal
## Perú · CRISP-DM + CNN · SIS210 Algoritmos y EDA

### Estructura del proyecto
```
vigia-satelital/
├── backend/          → API FastAPI + pipeline GEE (Persona A)
├── frontend/         → React + Leaflet geovisor    (Persona B)
├── notebooks/        → Google Colab entrenamiento  (Persona A)
├── datasets/
│   ├── raw/          → GeoTIFF descargados de GEE  (Persona C)
│   └── processed/    → Patches 512x512 listos      (Persona A)
└── models/           → Pesos .pth del modelo U-Net (Persona A)
```

### División del equipo
- Persona A → Backend Python, GEE, modelo U-Net
- Persona B → Frontend React, Leaflet, UI
- Persona C → Datasets, cuentas GEE/NICFI, documentación
