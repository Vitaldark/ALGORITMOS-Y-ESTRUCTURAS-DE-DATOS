Tablas Hash 

**Proyecto de SEMANA 5** - Algoritmos y Estructuras de Datos

En este proyecto exploramos y comparamos **dos formas diferentes de manejar colisiones en Tablas Hash**. Básicamente, cuando múltiples claves quieren ocupar el mismo lugar en la tabla, ¿qué hacemos?

1. **Encadenamiento Separado** : Guardamos todos los elementos en una lista en esa posición
2. **Sondeo Lineal** : Buscamos el siguiente espacio disponible en la tabla

Se implemento ambas en C++ y las pusimos a prueba con datos reales de transacciones comerciales para ver cuál funciona mejor en diferentes escenarios.

## Características Principales

-  Función hash personalizada (polinomial con base 31)
-  Lectura de datos desde archivo CSV
-  Cálculo de colisiones en tiempo real
-  Medición de tiempo de inserción en microsegundos
-  Análisis de factor de carga (λ = n/m)
-  Datos sintéticos como fallback
-  Comparativa detallada de desempeño
-  **BONUS**: Versión en Python con gráficos y visualización de resultados

## Lo que se encontrará aquí
SEMANA 5
 implementacion.cpp           # Versión en C++ 
 [python_version]            # Versión en Python con gráficos bonitos 
 data usada/
    data.csv                  # Dataset de transacciones reales (500K+ registros)
 output/                      # Resultados de la ejecución
 informe_tablas_hash.docx    # Documentación detallada
 README.md                    # Este archivo (leyéndolo ahora )


**Nota**: Contamos con dos versiones del proyecto:
 **C++**: Enfocada en el rendimiento y análisis de tiempo
 **Python**: Con visualizaciones gráficas para entender mejor los resultados

##  Requisitos & Setup

Para ejecutar este proyecto, se necesita:

-  **Compilador**: GCC 7.0+ (o equivalente como Clang)
-  **Sistema**: Windows, Linux, macOS (funciona en cualquier lado)
-  **Dependencias**: Solo librerías estándar de C++ (iostream, fstream, vector, list, chrono)


### Versión Python 

Si prefieres ver gráficos bonitos:
- Python 3.7+
- Librerías: pandas, matplotlib, numpy
- Instalación rápida: `pip install pandas matplotlib numpy`

## Compilación y Ejecución 

### Paso 1: Compilar

**Opción A - manualmente**:
```bash
g++ -Wall -Wextra -O2 -std=c++17 implementacion.cpp -o implementacion.exe
```

**Opción B - VS Code -**:
- Presiona `Ctrl+Shift+B` y listo 
- O ve a Terminal → Run Build Task

### Paso 2: Ejecutar

```bash
# Windows
.\implementacion.exe

**¿Qué ves?** Una tabla comparativa mostrando cómo se comportan ambas estrategias 

### Versión Python 

```bash
python benchmark_hash.py
```

Genera gráficos lindos mostrando la relación entre colisiones, tiempo y tamaño de tabla.


##  Los Datos (y por qué son importantes)

Usamos datos reales de transacciones de una tienda online. No inventamos nada. 

**Archivo**: `data usada/data.csv`

-  **Origen**: Transacciones reales de retail del 2010 (kaggle)
-  **Formato**: CSV (fácil de entender)
-  **Tamaño**: ~500,000 registros (bastante para hacer un benchmarks serio)
-  **Columna clave** (0): StockCode - El código del producto
-  **Columna valor** (1): Description - Descripción del producto

**¿Qué pasa si no tenemos el CSV?**
El programa es inteligente: genera automáticamente 5,000 registros sintéticos para que puedas testear igual. Así no te quedas sin nada. 

### Muestra del Dataset
```
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,12/1/2010 8:26,2.55,17850,United Kingdom
536365,71053,WHITE METAL LANTERN,6,12/1/2010 8:26,3.39,17850,United Kingdom
536365,84406B,CREAM CUPID HEARTS COAT HANGER,8,12/1/2010 8:26,2.75,17850,United Kingdom
...
```

---

## Salida Esperada 

Cuando ejecutes el programa, verás algo así:

```
=== BENCHMARK TABLAS HASH (C++) ===
Registros generados: 5000

m         n         Col_Enc    Ins_enc(us)  Col_SL     Ins_SL(us)
------------------------------------------------------------
1009      656       152        2500         89         1800
2003      1302      45         5100         12         3900
4001      2600      8          9800         2          7600
8009      5205      1          19000        0          15000
```

### ¿Qué significan estas letras raras? 

| Columna | Significado | ¿Por qué importa? |
|---------|-------------|-------------------|
| **m** | Tamaño de la tabla hash (siempre números primos) | Más grande = menos colisiones |
| **n** | Cuántos elementos insertamos (~65% de m) | Es el 65% del tamaño para un test justo |
| **Col_Enc** | Colisiones en encadenamiento | Menos es mejor, pero tolerable |
| **Ins_enc(us)** | Tiempo de inserción en C++ (microsegundos) | Queremos que sea rápido  |
| **Col_SL** | Colisiones en sondeo lineal | Tiene límite antes de explotar |
| **Ins_SL(us)** | Tiempo sondeo lineal (microsegundos) | Para comparar con el otro método |

**Conclusión del benchmark**: Verás cómo las tablas más grandes tienen menos colisiones pero más tiempo de acceso. Trade-off clásico. 

## Cosas Importantes que a Saber

### 1 La ruta del CSV está hardcodeada 
En el código tenemos:
```cpp
leerCSV("D:/INGENIERIA DE SISTEMAS/5to SEMESTRE/ALGORITMOS Y ESTRUCTURAS DE DATOS/SEMANA 5/data usada/data.csv", 0, 1);
```

**Solución**: En caso de no encontrar el archivo hacer:
- Opción A: Cambia la ruta en el código antes de compilar
- Opción B: Corre el programa y déjalo generar datos sintéticos

### 2 Los datos sintéticos 
Si no tienes el CSV, el programa automáticamente genera 5,000 registros fake pero válidos. Funciona perfectamente para testear.

### 3 Los tiempos varían según tu PC 
Si lo ejecutas en una computadora rápida vs una vieja, los microsegundos serán muy diferentes. **Lo importante es la relación entre columnas**, no los valores absolutos.


## Conceptos Clave 

- **Tabla Hash**: Es como un diccionario súper rápido. Das una clave, obtienes un valor al instante
- **Colisión**: Cuando dos claves diferentes quieren estar en el mismo lugar. ¡Conflicto! 
- **Encadenamiento**: Solución fácil: si hay conflicto, creas una lista en ese lugar
- **Sondeo Lineal**: Solución alternativa: si está ocupado, te vas al siguiente espacio disponible
- **Número Primo**: Mágica secreta para que la función hash funcione mejor

---

##  Contexto Académico

- **Asignatura**: Algoritmos y Estructuras de Datos
- **Semana**: 5-6
- **Tema**: Tablas Hash y gestión de colisiones
- **Profesor**: Aldo Hernán Zanabria Gálvez
- **Institución**: Universidad Nacional del Altiplano Puno (INGENIERÍA DE SISTEMAS)

##  El Equipo (3 cabezas pensantes + mucha motivacion por aprender )

- **Jesus Vidal Checma Montalvo** 
- **Francy Jimena Ramos Vilca** 
- **Emerson Aldair Flores Flores** 

## Fecha & Info

- **Fecha de entrega**: Mayo 2026
- **Versión**: 1.0
- **Estado**: Completado y funcionando 

## La Versión en Python 

No solo se encuentra la versión en C++, también implementamos todo en Python con:

- **Gráficos de colisiones** vs tamaño de tabla
- **Análisis de tiempos** con matplotlib
- **Exportación de resultados** a CSV
- **Visualización hermosa** de datos

## Licencia

Este proyecto es parte del curso de Algoritmos y Estructuras de Datos. Uso académico únicamente.

**¡Muchas gracias por leer! Si tienes dudas, revisa el código... todo está comentado.**
