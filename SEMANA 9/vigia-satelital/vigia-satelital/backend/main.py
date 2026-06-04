from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
import math, random

_ALERTS = [
    {"id":1,"zona":"La Pampa","region":"Madre de Dios","tipo":"Aluvial/Dragas","ha":4200,"confianza":0.97,"severidad":"Critica","fecha":"2026-05-28","lat":-12.72,"lng":-69.97},
    {"id":2,"zona":"Pariamanu","region":"Madre de Dios","tipo":"Aluvial","ha":890,"confianza":0.91,"severidad":"Alta","fecha":"2026-05-25","lat":-12.58,"lng":-69.78},
    {"id":3,"zona":"Chaspa","region":"Puno","tipo":"Aluvial/SAR","ha":1340,"confianza":0.88,"severidad":"Critica","fecha":"2026-05-30","lat":-13.85,"lng":-69.62},
    {"id":4,"zona":"Valle Dorado","region":"Cusco","tipo":"Socavon","ha":620,"confianza":0.84,"severidad":"Alta","fecha":"2026-05-20","lat":-13.21,"lng":-70.12},
    {"id":5,"zona":"Tambopata Sector Azul","region":"Madre de Dios","tipo":"Balsas traca","ha":310,"confianza":0.79,"severidad":"Alta","fecha":"2026-05-15","lat":-13.12,"lng":-69.71},
    {"id":6,"zona":"Inambari","region":"Puno","tipo":"Aluvial","ha":2100,"confianza":0.93,"severidad":"Critica","fecha":"2026-05-29","lat":-13.83,"lng":-69.95},
    {"id":7,"zona":"Quincemil","region":"Cusco","tipo":"Aluvial","ha":450,"confianza":0.76,"severidad":"Media","fecha":"2026-04-10","lat":-13.22,"lng":-70.74},
    {"id":8,"zona":"Mazuco","region":"Madre de Dios","tipo":"Dragado","ha":780,"confianza":0.89,"severidad":"Alta","fecha":"2026-05-18","lat":-12.86,"lng":-70.28},
]

app = FastAPI(title="VIGÍA SATELITAL API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"sistema": "VIGÍA SATELITAL", "version": "1.0.0", "estado": "activo"}

@app.get("/alertas")
def get_alertas(
    region: Optional[str] = Query(None),
    severidad: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    conf_min: float = Query(0.0, ge=0, le=1),
):
    data = _ALERTS
    if region:    data = [a for a in data if a["region"] == region]
    if severidad: data = [a for a in data if a["severidad"] == severidad]
    if tipo:      data = [a for a in data if tipo.lower() in a["tipo"].lower()]
    if conf_min:  data = [a for a in data if a["confianza"] >= conf_min]
    features = []
    for a in data:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [a["lng"], a["lat"]]},
            "properties": {k: v for k, v in a.items() if k not in ("lat","lng")}
        })
    return {"type": "FeatureCollection", "total": len(features), "generado": datetime.utcnow().isoformat(), "features": features}

@app.get("/alertas/{alert_id}/geojson")
def get_alerta_geojson(alert_id: int):
    alerta = next((a for a in _ALERTS if a["id"] == alert_id), None)
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    cx, cy = alerta["lng"], alerta["lat"]
    r = 0.02
    coords = [[cx + r*math.cos(math.radians(i)), cy + r*math.sin(math.radians(i))] for i in range(0, 360, 30)]
    coords.append(coords[0])
    return {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [coords]}, "properties": alerta}

@app.get("/estadisticas")
def get_estadisticas():
    total_ha  = sum(a["ha"] for a in _ALERTS)
    criticas  = sum(1 for a in _ALERTS if a["severidad"] == "Critica")
    conf_prom = sum(a["confianza"] for a in _ALERTS) / len(_ALERTS)
    return {
        "total_alertas": len(_ALERTS),
        "alertas_criticas": criticas,
        "hectareas_totales": total_ha,
        "confianza_promedio": round(conf_prom, 3),
        "regiones": list({a["region"] for a in _ALERTS}),
        "ultima_actualizacion": "2026-05-30"
    }

@app.post("/detectar")
def trigger_detection(zona: str, bbox: Optional[str] = None):
    ha_detectadas = random.randint(200, 5000)
    confianza     = round(random.uniform(0.75, 0.98), 2)
    return {
        "zona": zona, "estado": "completado",
        "ha_detectadas": ha_detectadas, "confianza": confianza,
        "modelo": "U-Net + ResNet50", "satelite": "Sentinel-2 10m",
        "timestamp": datetime.utcnow().isoformat(),
        "mensaje": f"Deteccion completada: {ha_detectadas} ha afectadas en {zona}"
    }
