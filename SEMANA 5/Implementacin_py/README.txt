📋 Descripción
Implementación y comparación de dos estrategias de resolución de colisiones en tablas hash:
- **Encadenamiento** — cada celda contiene una lista enlazada
- **Sondeo Lineal** — búsqueda secuencial del siguiente espacio libre
Se comparan ambas contra el `dict` nativo de Python como referencia de rendimiento.
---
## 📊 Dataset
- **Fuente:** [Kaggle — Online Retail Dataset]
- **Archivo:** `data usada/data.csv`
- **Codificación:** `latin-1`
- **Columna clave usada:** `InvoiceNo`
---
## ▶️ Ejecución
```bash
cd "SEMANA 5/Implementación_py"
python codde.py
```
> **Requisitos:** Python 3.10+, pandas, matplotlib
Instalar dependencias:
```bash
pip install pandas matplotlib
```
---
## 📈 Métricas Evaluadas
| Métrica | Descripción |
|---|---|
| `m` | Tamaño de la tabla hash |
| `n` | Número de elementos insertados |
| `lambda` | Factor de carga (n/m) |
| `ColEnc` | Colisiones en encadenamiento |
| `ColSL` | Colisiones en sondeo lineal |
| `InsEnc` | Tiempo de inserción — encadenamiento (ms) |
| `InsSL` | Tiempo de inserción — sondeo lineal (ms) |
| `InsPy` | Tiempo de inserción — dict Python (ms) |
| `BusEnc` | Tiempo de búsqueda — encadenamiento (ms) |
| `BusSL` | Tiempo de búsqueda — sondeo lineal (ms) |
Tamaños evaluados: `m = 1009, 2003, 4001, 8009` (números primos)
---
## ⚙️ Función Hash Utilizada
```python
def funcion_hash(clave, tamanio):
    hash_val = 0
    for c in str(clave):
        hash_val = (hash_val * 31 + ord(c)) % tamanio
    return hash_val
```
Polinomio de base 31 sobre los caracteres de la clave — estándar en implementaciones de propósito general.
---
## 🔍 Observaciones
- El **sondeo lineal** genera más colisiones que el encadenamiento con el mismo factor de carga, debido al fenómeno de **clustering primario**
- El **encadenamiento** es más tolerante a factores de carga altos (> 0.7)
- El `dict` de Python supera a ambas implementaciones por usar una función hash en C optimizada internamente
- El sondeo lineal se limita a un factor de carga máximo de **0.75** para evitar degradación severa
---
## 👤 Enero.dev

**[Flores Flores Emerson Aldair]**
[Ramos Vilca Francy Jimena]
[Checma Montalvo Jesus Vidal]
Quinto Semestre — Algoritmos y Estructuras de Datos
