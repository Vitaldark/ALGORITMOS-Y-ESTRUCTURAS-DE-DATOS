# Mini Hoja de Cálculo Académica (C++ & Python)

¡Bienvenido! Este repositorio contiene una aplicación de consola interactiva que simula una **Mini Hoja de Cálculo Académica** para la gestión de estudiantes, notas y analíticas. El proyecto está implementado de forma nativa tanto en **C++** como en **Python**, aplicando estructuras de datos avanzadas y algoritmos fundamentales de las ciencias de la computación para garantizar un rendimiento óptimo.

Es una herramienta ideal para entender cómo funcionan las estructuras indexadas, la persistencia de estados en memoria (Undo) y los sistemas de atención basados en colas.

---

## Características Principales

* **Gestión de Registros (Filas):** Inserción de estudiantes con validación en tiempo real de calificaciones en el rango de `[0, 20]`.
* **Indexación en Tiempo O(1):** Uso de Tablas Hash asociativas para búsquedas inmediatas por código único de estudiante y prevención de claves duplicadas.
* **Sistema de Deshacer (Undo):** Historial de modificaciones respaldado por una estructura de Pila (`Stack`), permitiendo revertir el último cambio de estado.
* **Cola de Atención FIFO:** Flujo secundario mediante una Estructura de Cola (`Queue`) para simular la atención secuencial de estudiantes en secretaría.
* **Algoritmos de Ordenamiento Avanzados:**
    * **QuickSort:** Clasificación descendente (de mayor a menor) basada en el promedio de notas.
    * **MergeSort:** Clasificación ascendente (alfanumérica) basada de forma estable en el código del estudiante.
* **Métricas Analíticas:** Procesamiento estadístico (recursivo e iterativo) para obtener el promedio general del cohorte e identificar los rendimientos más altos y bajos.

---

## Estructura de Datos y Arquitectura

El proyecto demuestra la equivalencia de conceptos lógicos implementados en dos lenguajes de programación distintos:

| Componente Lógico | Implementación en C++ (`FINAL.cpp`) | Implementación en Python (`FINAL.py`) | Complejidad / Propósito |
| :--- | :--- | :--- | :--- |
| **Registro Base** | `struct Estudiante` | Diccionarios nativos (`dict`) | Representación de la fila/celda. |
| **Matriz Principal** | `std::vector<Estudiante>` | Listas dinámicas (`[]`) | Almacenamiento secuencial activo. |
| **Índice de Búsqueda**| `std::unordered_map` | Tablas Hash nativas (`{}`) | Búsqueda y validación en **O(1)**. |
| **Historial (Undo)** | `std::stack<vector<Estudiante>>`| Listas dinámicas (`.append()` / `.pop()`) | Copias de seguridad del estado de la hoja. |
| **Cola de Espera** | `std::queue<string>` | Doble cola eficiente (`collections.deque`) | Flujo institucional **FIFO** (First-In, First-Out). |

---
---

## Anexos: Capturas de Pantalla (Simulación en VS Code)

Las siguientes imágenes muestran el comportamiento real del sistema tras ser compilado y ejecutado desde el entorno de **Visual Studio Code**.

| 1. Registro de Estudiantes y Formato de Tabla |
<img width="396" height="160" alt="Registro cpp" src="https://github.com/user-attachments/assets/65b8ea39-4caf-454f-924c-9bdcee49599d" />

| 2. Búsquedas O(1) e Índices Hash |
<img width="471" height="97" alt="Busqueda" src="https://github.com/user-attachments/assets/776caeba-3d79-4555-83fd-d2e8fb3c6094" />

| 3. Aplicación de QuickSort y MergeSort 
<img width="449" height="182" alt="Quicksort" src="https://github.com/user-attachments/assets/7c28bcc4-1102-44f5-a1c8-563352b066ea" />
<img width="437" height="166" alt="Mergesort" src="https://github.com/user-attachments/assets/7169cfb4-9a1b-41a9-8c93-c9a3bf6cc1cd" />

| 4. Cola de Atención (FIFO) y Sistema Undo |
<img width="441" height="131" alt="atencion2" src="https://github.com/user-attachments/assets/37aec8c2-7053-4950-a10f-1c1b72a25f53" />
<img width="444" height="164" alt="atencion1" src="https://github.com/user-attachments/assets/a9766ea7-dce3-4f8c-8145-aeba2a889c94" />

| 5. Reporte Estadístico y Métricas Analíticas |
<img width="458" height="127" alt="Reporte" src="https://github.com/user-attachments/assets/7fe9dd89-88b9-4780-9f95-0f34104aea65" />

---

## 👤 Información del Autor

Este proyecto fue desarrollado como parte del trabajo académico en algoritmos y estructuras de datos.

* **Nombre Completo:** Jesus Vidal Checma Montalvo
* **Código de Estudiante:** 240143
* **Institución:** Universidad Nacional del Altiplano (UNAP)
* **Facultad / Escuela:** Ingeniería de Sistemas 

---
*Desarrollado con fines educativos para el análisis del rendimiento algorítmico.*
---

## Requisitos del Sistema

### Para la versión en C++
* Un compilador que soporte **C++11** o superior (GCC, Clang o MSVC).
* Herramientas de entorno como `g++` instaladas en la terminal.

### Para la versión en Python
* **Python 3.x** instalado.
* No requiere librerías externas de terceros (únicamente módulos de la biblioteca estándar como `collections` y `copy`).

---

## Instrucciones de Ejecución

### Opción 1: Compilar y Ejecutar en C++
Abre tu terminal en la carpeta raíz del proyecto y ejecuta los siguientes comandos:

```bash
# Compilación del archivo fuente
g++ -O3 FINAL.cpp -o MiniSpreadsheet

# Ejecución del binario compilado
./MiniSpreadsheet

