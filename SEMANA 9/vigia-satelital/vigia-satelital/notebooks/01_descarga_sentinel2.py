# VIGIA SATELITAL — Notebook 1: Descarga Sentinel-2
# Ejecutar en Google Colab (Runtime > Change runtime type > GPU T4)

# CELDA 1: Instalar
# !pip install earthengine-api geemap rasterio numpy matplotlib

# CELDA 2: Autenticar
import ee
# ee.Authenticate()   # descomentar la primera vez
ee.Initialize(project='TU-PROJECT-ID')
print("GEE conectado OK")

# CELDA 3: Zonas de estudio Peru
ZONAS = {
    "la_pampa":  {"bbox": [-70.10, -12.85, -69.85, -12.60], "nombre": "La Pampa, Madre de Dios"},
    "chaspa":    {"bbox": [-69.80, -14.10, -69.55, -13.85], "nombre": "Chaspa, Puno"},
    "inambari":  {"bbox": [-70.15, -14.00, -69.90, -13.75], "nombre": "Inambari, Puno"},
}

# CELDA 4: Funcion de descarga con mascara de nubes
def descargar_s2(zona_key, fecha_ini, fecha_fin, carpeta="vigia_datasets"):
    zona   = ZONAS[zona_key]
    region = ee.Geometry.Rectangle(zona["bbox"])

    def mask_clouds(img):
        scl  = img.select('SCL')
        mask = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10))
        return img.updateMask(mask).divide(10000)

    col = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterBounds(region)
           .filterDate(fecha_ini, fecha_fin)
           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
           .map(mask_clouds)
           .select(['B4','B3','B2','B8'])
           .median()
           .clip(region))

    nombre = f"s2_{zona_key}_{fecha_ini[:4]}"
    tarea  = ee.batch.Export.image.toDrive(
        image=col, description=nombre, folder=carpeta,
        scale=10, region=region, fileFormat='GeoTIFF', maxPixels=1e10
    )
    tarea.start()
    print(f"Exportando: {zona['nombre']} -> Drive/{carpeta}/{nombre}.tif")
    return tarea

# CELDA 5: Ejecutar para todas las zonas (epoca seca)
for z in ZONAS.keys():
    descargar_s2(z, '2024-06-01', '2024-08-31')

print("Revisar tareas: https://code.earthengine.google.com/ -> Tasks")
