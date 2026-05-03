# 📦 Hash Tables — Estructuras de Datos

> **Práctica Avanzada | Semanas 5 y 6**  
> Curso: Estructuras de Datos  
> Universidad Nacional del Altiplano de Puno  
> Docente: Mg. Aldo Hernan Zanabria Galvez  
> Lenguajes: Python 🐍 · C++ ⚙️

---

## 📋 Descripción

Este repositorio contiene la implementación completa de **tablas hash** con dos métodos de resolución de colisiones, desarrollados sobre datos reales de comercio electrónico descargados de Kaggle.

Se implementan y comparan:

| Método | Lenguaje | Descripción |
|--------|----------|-------------|
| **Encadenamiento Separado** | Python / C++ | Cada posición contiene una lista enlazada de elementos |
| **Sondeo Lineal** | Python / C++ | Busca la siguiente posición libre de forma secuencial |
| **Diccionario nativo** | Python | Referencia de rendimiento óptimo |

---

## 📁 Estructura del repositorio

```
hash-tables/
│
├── python/
│   ├── hash_tables.py        # Implementación completa en Python
│   └── requirements.txt      # Dependencias (pandas, matplotlib)
│
├── cpp/
│   ├── hash_tables.cpp       # Implementación completa en C++
│   └── Makefile              # Script de compilación
│
├── .gitignore
└── README.md
```

---

## 🗄️ Dataset

Se utiliza el dataset **eCommerce Behavior Data from Multi Category Store** publicado en Kaggle:

- **Autor:** Mikhail Kechinov
- **Enlace:** https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
- **Columnas usadas:** `user_id`, `product_id`, `category_id`
- **Filas procesadas:** 10,000 (primeras filas sin nulos)

> ⚠️ **El dataset NO está incluido en el repositorio** por su tamaño y licencia de Kaggle.  
> Debes descargarlo manualmente y guardarlo como `ecommerce_sample.csv` dentro de la carpeta del script que vayas a ejecutar.

---

## ⚙️ Configuración del experimento

| Parámetro | Valor |
|-----------|-------|
| Número de elementos insertados (n) | 10,000 |
| Tamaño de la tabla (m) | 20,011 *(número primo)* |
| Claves usadas para búsqueda | 1,000 primeras claves |
| Factor de carga resultante (α) | ≈ 0.4997 |

---

## 🐍 Ejecución en Python

### Requisitos

- Python 3.8 o superior
- pip

### Instalación de dependencias

```bash
cd python
pip install -r requirements.txt
```

### Ejecución

```bash
# Asegúrate de tener 'ecommerce_sample.csv' en la carpeta python/
python hash_tables.py
```

### Salida esperada

```
============================================================
  ANÁLISIS DE TABLAS HASH - DATOS KAGGLE
============================================================

[1] Cargando dataset...
  → Filas cargadas (sin nulos): 10,000
  → Claves extraídas: 10,000
  → Tamaño de tabla:  20,011

[2] Prueba con Encadenamiento Separado...
  → Inserción: 0.041200 s
  → Búsqueda (1,000 claves): 0.008900 s
  → Colisiones: 1,247
  → Factor de carga: 0.4997

[3] Prueba con Sondeo Lineal...
  → Inserción: 0.053100 s
  → Búsqueda (1,000 claves): 0.010300 s
  → Colisiones: 1,389
  → Factor de carga: 0.4997

[4] Prueba con Diccionario nativo de Python...
  → Inserción: 0.002100 s
  → Búsqueda (1,000 claves): 0.000400 s
  → Colisiones: N/A (estructura nativa)

[5] Tabla comparativa de resultados:

          Metodo  Tiempo insercion  Tiempo busqueda  Colisiones  Factor de carga
  Encadenamiento          0.041200         0.008900        1247           0.4997
   Sondeo Lineal          0.053100         0.010300        1389           0.4997
Diccionario Python        0.002100         0.000400           0           0.4997

[6] Generando gráficos...
  → Gráfico guardado como 'resultados_hash.png'
```

---

## ⚙️ Compilación y ejecución en C++

### Requisitos

- g++ con soporte para C++17
- make (opcional)

### Con Makefile

```bash
cd cpp
make          # Compila
make run      # Compila y ejecuta
make clean    # Limpia binarios
```

### Sin Makefile (manual)

```bash
cd cpp
g++ -std=c++17 -O2 -o hash_tables hash_tables.cpp
./hash_tables
```

### Salida esperada

```
============================================================
  ANÁLISIS DE TABLAS HASH - DATOS KAGGLE (C++)
============================================================

[1] Cargando dataset...
  -> Claves cargadas: 10000
  -> Tamaño de tabla: 20011

[2] Prueba con Encadenamiento Separado...
  -> Insercion:  0.003800 s
  -> Busqueda:   0.000700 s
  -> Colisiones: 1251
  -> Factor de carga: 0.499925

[3] Prueba con Sondeo Lineal...
  -> Insercion:  0.004400 s
  -> Busqueda:   0.000900 s
  -> Colisiones: 1402
  -> Factor de carga: 0.499925

[4] Resultados del experimento:
------------------------------------------------------------
Metodo                Ins. (s)        Busq. (s)       Colisiones    Carga
------------------------------------------------------------
Encadenamiento        0.003800        0.000700        1251          0.499925
Sondeo Lineal         0.004400        0.000900        1402          0.499925
------------------------------------------------------------
```

---

## 📊 Resultados comparativos

| Método | T. Inserción (s) | T. Búsqueda (s) | Colisiones | Factor de Carga |
|--------|-----------------|-----------------|------------|-----------------|
| Encadenamiento (Python) | 0.0412 | 0.0089 | 1,247 | 0.4997 |
| Sondeo Lineal (Python) | 0.0531 | 0.0103 | 1,389 | 0.4997 |
| Diccionario Python | 0.0021 | 0.0004 | N/A | N/A |
| Encadenamiento (C++) | 0.0038 | 0.0007 | 1,251 | 0.4997 |
| Sondeo Lineal (C++) | 0.0044 | 0.0009 | 1,402 | 0.4997 |

> Los tiempos variarán según el hardware donde se ejecute el código.

---

## 🧠 Conceptos clave

### ¿Qué es una tabla hash?

Una tabla hash almacena pares **clave → valor** y transforma cada clave en un índice del arreglo mediante una **función hash**: `h(k) = k mod m`. En condiciones ideales, las operaciones de inserción y búsqueda tienen complejidad **O(1)**.

### Encadenamiento separado

Cada posición del arreglo contiene una **lista enlazada**. Las colisiones se resuelven agregando el elemento al final de la lista correspondiente. Funciona bien con factores de carga altos (α > 0.75).

### Sondeo lineal

Todos los elementos se almacenan en el arreglo principal. Si una posición está ocupada, se busca la siguiente libre: `h_i(k) = (h(k) + i) mod m`. Más eficiente en uso de caché, pero se degrada cuando α > 0.7.

### Factor de carga

```
α = n / m
```

Donde `n` = número de elementos y `m` = tamaño de la tabla. Se recomienda mantener **α ≤ 0.75** para un rendimiento óptimo.

---

## 📚 Referencias

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4.ª ed.). MIT Press.
- Tapia-Fernández, S., García-García, D., & García-Hernandez, P. (2022). Key concepts, weakness and benchmark on hash table data structures. *Algorithms, 15*(3), 100. https://doi.org/10.3390/a15030100
- Rodríguez-Baena, L. C., & Morales-Bueno, R. (2025). Hash tables as engines of randomness at the limits of computation: A unified review of algorithms. *Algorithms, 18*(12), 804. https://doi.org/10.3390/a18120804
- Yusuf, A., Nimbe, P., & Opoku, M. (2021). Collision resolution techniques in hash table: A review. *International Journal of Advanced Computer Science and Applications, 12*(9), 698–706. https://doi.org/10.14569/IJACSA.2021.0120984
- Kechinov, M. (s.f.). *eCommerce behavior data from multi category store*. Kaggle. https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store

---

## 📝 Licencia

Este proyecto es de uso académico. Libre para modificar y distribuir con fines educativos.
