"""
=============================================================================
Implementación de Tablas Hash en Python
=============================================================================
Práctica Avanzada - Estructuras de Datos (Semanas 5 y 6)
Universidad Nacional del Altiplano de Puno
Docente: Mg. Aldo Hernan Zanabria Galvez

Descripción:
    Implementa y compara tres estrategias de indexación:
      1. Tabla Hash con Encadenamiento Separado
      2. Tabla Hash con Sondeo Lineal
      3. Diccionario nativo de Python (referencia de rendimiento)

Dataset:
    eCommerce Behavior Data from Multi Category Store
    Autor: Mikhail Kechinov
    Fuente: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store

Uso:
    1. Descarga el dataset de Kaggle y guárdalo como 'ecommerce_sample.csv'
       en la misma carpeta que este archivo.
    2. Ejecuta: python hash_tables.py

Dependencias:
    pip install pandas matplotlib
=============================================================================
"""

import pandas as pd
import time
import matplotlib.pyplot as plt
from typing import List, Tuple, Any, Optional


# =============================================================================
# CLASE 1: Tabla Hash con Encadenamiento Separado
# =============================================================================

class HashTableChaining:
    """
    Tabla hash que resuelve colisiones mediante encadenamiento separado.

    Cada posición del arreglo interno contiene una lista de pares (clave, valor).
    Cuando dos claves generan el mismo índice (colisión), el nuevo elemento
    se agrega al final de la lista correspondiente.

    Complejidad promedio:
        - Inserción: O(1)
        - Búsqueda:  O(1 + α)  donde α es el factor de carga
        - Eliminación: O(1 + α)
    """

    def __init__(self, size: int):
        """
        Inicializa la tabla hash.

        Args:
            size (int): Número de posiciones de la tabla.
                        Se recomienda usar un número primo para
                        mejorar la distribución de las claves.
        """
        self.size = size
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(size)]
        self.collisions = 0

    def hash_function(self, key) -> int:
        """
        Calcula el índice de una clave dentro de la tabla.

        Usa la función hash built-in de Python seguida de una operación
        módulo para obtener un índice válido.

        Args:
            key: La clave a transformar (cualquier tipo hashable).

        Returns:
            int: Índice entre 0 y self.size - 1.
        """
        return hash(str(key)) % self.size

    def insert(self, key, value) -> None:
        """
        Inserta un par (clave, valor) en la tabla hash.

        Si la posición calculada ya tiene elementos, se registra
        una colisión y el nuevo elemento se agrega a la lista.

        Args:
            key:   La clave de búsqueda.
            value: El valor asociado a la clave.
        """
        index = self.hash_function(key)

        # Si la lista en esa posición ya tiene elementos -> hay colisión
        if len(self.table[index]) > 0:
            self.collisions += 1

        self.table[index].append((key, value))

    def search(self, key):
        """
        Busca un valor por su clave.

        Calcula el índice de la clave y recorre la lista en esa
        posición hasta encontrar la clave exacta.

        Args:
            key: La clave a buscar.

        Returns:
            El valor asociado a la clave, o None si no existe.
        """
        index = self.hash_function(key)

        for k, v in self.table[index]:
            if k == key:
                return v

        return None  # Clave no encontrada

    def delete(self, key) -> bool:
        """
        Elimina un par (clave, valor) de la tabla.

        Args:
            key: La clave a eliminar.

        Returns:
            bool: True si se eliminó, False si la clave no existía.
        """
        index = self.hash_function(key)

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                return True

        return False

    def load_factor(self, total_elements: int) -> float:
        """
        Calcula el factor de carga α = n / m.

        Args:
            total_elements (int): Número de elementos insertados (n).

        Returns:
            float: Factor de carga entre 0.0 y 1.0 (o mayor si hay encadenamiento).
        """
        return total_elements / self.size

    def __repr__(self) -> str:
        return (f"HashTableChaining(size={self.size}, "
                f"collisions={self.collisions})")


# =============================================================================
# CLASE 2: Tabla Hash con Sondeo Lineal
# =============================================================================

class HashTableLinearProbing:
    """
    Tabla hash de direccionamiento abierto con sondeo lineal.

    Todos los elementos se almacenan directamente en el arreglo principal,
    sin estructuras auxiliares. Cuando una posición está ocupada, el
    algoritmo explora la siguiente posición disponible secuencialmente:

        h_i(k) = (h(k) + i) mod m,   i = 0, 1, 2, ...

    Complejidad promedio (con α < 0.5):
        - Inserción: O(1)
        - Búsqueda:  O(1 / (1 - α))
        - Eliminación: O(1 / (1 - α))

    Advertencia:
        El rendimiento se degrada significativamente cuando α > 0.7
        debido al fenómeno de agrupamiento primario.
    """

    def __init__(self, size: int):
        """
        Inicializa la tabla hash.

        Args:
            size (int): Capacidad máxima de la tabla. Debe ser mayor
                        al número de elementos que se insertarán.
        """
        self.size = size
        self.table: List[Optional[Tuple[Any, Any]]] = [None] * size
        self.collisions = 0

    def hash_function(self, key) -> int:
        """
        Calcula el índice inicial de una clave.

        Args:
            key: La clave a transformar.

        Returns:
            int: Índice entre 0 y self.size - 1.
        """
        return hash(str(key)) % self.size

    def insert(self, key, value) -> None:
        """
        Inserta un par (clave, valor) usando sondeo lineal.

        Si la posición inicial está ocupada, avanza secuencialmente
        hasta encontrar una posición libre. Cada intento fallido
        incrementa el contador de colisiones.

        Args:
            key:   La clave de búsqueda.
            value: El valor asociado.

        Raises:
            OverflowError: Si la tabla está completamente llena.
        """
        index = self.hash_function(key)
        start = index

        while self.table[index] is not None:
            self.collisions += 1
            index = (index + 1) % self.size

            # Si dimos la vuelta completa, la tabla está llena
            if index == start:
                raise OverflowError("La tabla hash está llena. "
                                    "Considera aumentar su tamaño.")

        self.table[index] = (key, value)

    def search(self, key):
        """
        Busca un valor usando sondeo lineal.

        Calcula el índice inicial y avanza hasta encontrar la clave
        o una posición vacía (lo que significa que la clave no existe).

        Args:
            key: La clave a buscar.

        Returns:
            El valor asociado a la clave, o None si no existe.
        """
        index = self.hash_function(key)
        start = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]

            index = (index + 1) % self.size

            # Evitar bucle infinito
            if index == start:
                break

        return None

    def load_factor(self, total_elements: int) -> float:
        """
        Calcula el factor de carga α = n / m.

        Args:
            total_elements (int): Número de elementos insertados.

        Returns:
            float: Factor de carga. Debe mantenerse < 0.7 para
                   un rendimiento óptimo con sondeo lineal.
        """
        return total_elements / self.size

    def __repr__(self) -> str:
        return (f"HashTableLinearProbing(size={self.size}, "
                f"collisions={self.collisions})")


# =============================================================================
# FUNCIÓN: Graficar resultados comparativos
# =============================================================================

def plot_results(results: pd.DataFrame) -> None:
    """
    Genera dos gráficos de barras comparando los métodos evaluados.

    Args:
        results (pd.DataFrame): DataFrame con columnas:
            'Metodo', 'Tiempo insercion', 'Tiempo busqueda',
            'Colisiones', 'Factor de carga'.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # --- Gráfico 1: Tiempo de inserción ---
    axes[0].bar(results["Metodo"], results["Tiempo insercion"],
                color=["#2E5496", "#C55A11", "#538135"])
    axes[0].set_title("Comparación de tiempo de inserción", fontsize=13)
    axes[0].set_xlabel("Método")
    axes[0].set_ylabel("Tiempo (segundos)")
    axes[0].tick_params(axis='x', rotation=15)

    # --- Gráfico 2: Tiempo de búsqueda ---
    axes[1].bar(results["Metodo"], results["Tiempo busqueda"],
                color=["#2E5496", "#C55A11", "#538135"])
    axes[1].set_title("Comparación de tiempo de búsqueda", fontsize=13)
    axes[1].set_xlabel("Método")
    axes[1].set_ylabel("Tiempo (segundos)")
    axes[1].tick_params(axis='x', rotation=15)

    plt.tight_layout()
    plt.savefig("resultados_hash.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("  -> Gráfico guardado como 'resultados_hash.png'")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():
    print("=" * 60)
    print("  ANÁLISIS DE TABLAS HASH - DATOS KAGGLE")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. Cargar y limpiar el dataset
    # ------------------------------------------------------------------
    print("\n[1] Cargando dataset...")
    import os
    
    # Buscar archivos CSV en el directorio Data (dos niveles arriba)
    data_dir = os.path.join(os.path.dirname(__file__), "..", "Data")
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    
    if not csv_files:
        print("\n  ERROR: No se encontraron archivos CSV en la carpeta Data.")
        return
    
    # Usar el primer archivo CSV encontrado
    csv_path = os.path.join(data_dir, csv_files[0])
    
    try:
        print(f"  -> Leyendo: {csv_files[0]}")
        df = pd.read_csv(csv_path, encoding='utf-8')
    except Exception as e:
        print(f"\n  ERROR: No se pudo leer el archivo: {e}\n")
        return

    df = df.dropna()
    print(f"  -> Filas cargadas (sin nulos): {len(df):,}")

    # ------------------------------------------------------------------
    # 2. Extraer claves (primeros 10,000 user_id)
    # ------------------------------------------------------------------
    keys = df["user_id"].astype(str).head(10_000).tolist()
    TABLE_SIZE = 20_011  # Número primo para mejor distribución

    print(f"  -> Claves extraídas: {len(keys):,}")
    print(f"  -> Tamaño de tabla:  {TABLE_SIZE:,}")

    # ------------------------------------------------------------------
    # 3. Prueba: Encadenamiento Separado
    # ------------------------------------------------------------------
    print("\n[2] Prueba con Encadenamiento Separado...")
    hash_chain = HashTableChaining(TABLE_SIZE)

    start = time.time()
    for key in keys:
        hash_chain.insert(key, {"user_id": key})
    insert_time_chain = time.time() - start

    start = time.time()
    for key in keys[:1_000]:
        hash_chain.search(key)
    search_time_chain = time.time() - start

    print(f"  -> Inserción: {insert_time_chain:.6f} s")
    print(f"  -> Búsqueda (1,000 claves): {search_time_chain:.6f} s")
    print(f"  -> Colisiones: {hash_chain.collisions:,}")
    print(f"  -> Factor de carga: {hash_chain.load_factor(len(keys)):.4f}")

    # ------------------------------------------------------------------
    # 4. Prueba: Sondeo Lineal
    # ------------------------------------------------------------------
    print("\n[3] Prueba con Sondeo Lineal...")
    hash_linear = HashTableLinearProbing(TABLE_SIZE)

    start = time.time()
    for key in keys:
        hash_linear.insert(key, {"user_id": key})
    insert_time_linear = time.time() - start

    start = time.time()
    for key in keys[:1_000]:
        hash_linear.search(key)
    search_time_linear = time.time() - start

    print(f"  -> Inserción: {insert_time_linear:.6f} s")
    print(f"  -> Búsqueda (1,000 claves): {search_time_linear:.6f} s")
    print(f"  -> Colisiones: {hash_linear.collisions:,}")
    print(f"  -> Factor de carga: {hash_linear.load_factor(len(keys)):.4f}")

    # ------------------------------------------------------------------
    # 5. Prueba: Diccionario nativo de Python (referencia)
    # ------------------------------------------------------------------
    print("\n[4] Prueba con Diccionario nativo de Python...")
    native_dict = {}

    start = time.time()
    for key in keys:
        native_dict[key] = {"user_id": key}
    insert_time_dict = time.time() - start

    start = time.time()
    for key in keys[:1_000]:
        native_dict.get(key)
    search_time_dict = time.time() - start

    print(f"  -> Inserción: {insert_time_dict:.6f} s")
    print(f"  -> Búsqueda (1,000 claves): {search_time_dict:.6f} s")
    print(f"  -> Colisiones: N/A (estructura nativa)")

    # ------------------------------------------------------------------
    # 6. Tabla comparativa de resultados
    # ------------------------------------------------------------------
    print("\n[5] Tabla comparativa de resultados:")
    results = pd.DataFrame({
        "Metodo": [
            "Encadenamiento",
            "Sondeo Lineal",
            "Diccionario Python"
        ],
        "Tiempo insercion": [
            insert_time_chain,
            insert_time_linear,
            insert_time_dict
        ],
        "Tiempo busqueda": [
            search_time_chain,
            search_time_linear,
            search_time_dict
        ],
        "Colisiones": [
            hash_chain.collisions,
            hash_linear.collisions,
            0
        ],
        "Factor de carga": [
            hash_chain.load_factor(len(keys)),
            hash_linear.load_factor(len(keys)),
            len(keys) / TABLE_SIZE
        ]
    })

    print()
    print(results.to_string(index=False))

    # ------------------------------------------------------------------
    # 7. Generar gráficos
    # ------------------------------------------------------------------
    print("\n[6] Generando gráficos...")
    plot_results(results)

    print("\n" + "=" * 60)
    print("  Ejecución completada exitosamente.")
    print("=" * 60)


if __name__ == "__main__":
    main()
