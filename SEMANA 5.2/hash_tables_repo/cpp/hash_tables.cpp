/*
=============================================================================
  Implementación de Tablas Hash en C++
=============================================================================
  Práctica Avanzada - Estructuras de Datos (Semanas 5 y 6)
  Universidad Nacional del Altiplano de Puno
  Docente: Mg. Aldo Hernan Zanabria Galvez

  Descripción:
    Implementa y compara dos estrategias de resolución de colisiones:
      1. Tabla Hash con Encadenamiento Separado (HashTableChaining)
      2. Tabla Hash con Sondeo Lineal (HashTableLinear)

  Dataset:
    eCommerce Behavior Data from Multi Category Store
    Autor: Mikhail Kechinov
    Fuente: https://www.kaggle.com/datasets/mkechinov/
            ecommerce-behavior-data-from-multi-category-store

  Compilación:
    g++ -std=c++17 -O2 -o hash_tables hash_tables.cpp

  Uso:
    ./hash_tables
    (El archivo 'ecommerce_sample.csv' debe estar en el mismo directorio)

  Dependencias:
    Biblioteca estándar de C++17 (no requiere instalaciones externas)
=============================================================================
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <list>
#include <chrono>
#include <string>
#include <iomanip>

using namespace std;
using namespace chrono;


// =============================================================================
// ESTRUCTURA: Registro clave-valor
// =============================================================================

/**
 * @brief Par clave-valor almacenado en la tabla hash.
 */
struct Record {
    string key;    ///< Clave de búsqueda (ej. user_id como string)
    string value;  ///< Valor asociado a la clave
};


// =============================================================================
// CLASE 1: Tabla Hash con Encadenamiento Separado
// =============================================================================

/**
 * @brief Tabla hash que resuelve colisiones mediante listas enlazadas.
 *
 * Cada posición del vector interno contiene una std::list<Record>.
 * Cuando dos claves generan el mismo índice (colisión), el nuevo
 * elemento se agrega al final de la lista correspondiente.
 *
 * Complejidad promedio:
 *   - Inserción: O(1)
 *   - Búsqueda:  O(1 + α)  donde α = n/m es el factor de carga
 */
class HashTableChaining {
private:
    int size;                          ///< Número de posiciones de la tabla
    vector<list<Record>> table;        ///< Vector de listas enlazadas
    int collisions;                    ///< Contador de colisiones registradas

public:

    /**
     * @brief Constructor.
     * @param tableSize Tamaño de la tabla. Se recomienda un número primo.
     */
    explicit HashTableChaining(int tableSize)
        : size(tableSize), collisions(0) {
        table.resize(size);
    }

    /**
     * @brief Función hash polinomial para cadenas.
     *
     * Calcula: hash = Σ(c * 31^i) mod m
     * El multiplicador 31 es un primo pequeño que minimiza colisiones
     * en distribuciones típicas de cadenas.
     *
     * @param  key Clave de tipo string.
     * @return Índice entre 0 y size - 1.
     */
    int hashFunction(const string& key) const {
        unsigned long hashVal = 0;
        for (char c : key) {
            hashVal = hashVal * 31 + static_cast<unsigned char>(c);
        }
        return static_cast<int>(hashVal % static_cast<unsigned long>(size));
    }

    /**
     * @brief Inserta un registro en la tabla hash.
     *
     * Si la posición ya contiene elementos se registra una colisión,
     * pero el nuevo elemento siempre se agrega a la lista.
     *
     * @param key   Clave del registro.
     * @param value Valor asociado.
     */
    void insert(const string& key, const string& value) {
        int index = hashFunction(key);

        if (!table[index].empty()) {
            collisions++;
        }

        table[index].push_back({key, value});
    }

    /**
     * @brief Busca un registro por su clave.
     *
     * @param  key Clave a buscar.
     * @return Valor asociado si se encontró, "No encontrado" en caso contrario.
     */
    string search(const string& key) const {
        int index = hashFunction(key);

        for (const Record& r : table[index]) {
            if (r.key == key) {
                return r.value;
            }
        }

        return "No encontrado";
    }

    /**
     * @brief Elimina un registro por su clave.
     *
     * @param  key Clave a eliminar.
     * @return true si se eliminó, false si no existía.
     */
    bool remove(const string& key) {
        int index = hashFunction(key);

        for (auto it = table[index].begin(); it != table[index].end(); ++it) {
            if (it->key == key) {
                table[index].erase(it);
                return true;
            }
        }

        return false;
    }

    /** @return Número total de colisiones registradas. */
    int getCollisions() const { return collisions; }

    /**
     * @brief Calcula el factor de carga α = n / m.
     * @param  totalElements Número de elementos insertados (n).
     * @return Factor de carga como valor decimal.
     */
    double loadFactor(int totalElements) const {
        return static_cast<double>(totalElements) / size;
    }
};


// =============================================================================
// CLASE 2: Tabla Hash con Sondeo Lineal
// =============================================================================

/**
 * @brief Tabla hash de direccionamiento abierto con sondeo lineal.
 *
 * Todos los elementos se almacenan directamente en el arreglo principal.
 * Cuando una posición está ocupada, el algoritmo busca la siguiente
 * posición libre de forma secuencial:
 *
 *   h_i(k) = (h(k) + i) mod m,   i = 0, 1, 2, ...
 *
 * Nota: El rendimiento se degrada cuando α > 0.7 por agrupamiento primario.
 */
class HashTableLinear {
private:
    int size;                    ///< Capacidad total de la tabla
    vector<Record> table;        ///< Arreglo principal de registros
    vector<bool> occupied;       ///< Marcas de ocupación por posición
    int collisions;              ///< Contador de intentos fallidos

public:

    /**
     * @brief Constructor.
     * @param tableSize Capacidad de la tabla. Debe superar al número
     *                  de elementos que se insertarán.
     */
    explicit HashTableLinear(int tableSize)
        : size(tableSize), collisions(0) {
        table.resize(size);
        occupied.assign(size, false);
    }

    /**
     * @brief Función hash polinomial (idéntica a HashTableChaining).
     *
     * @param  key Clave de tipo string.
     * @return Índice entre 0 y size - 1.
     */
    int hashFunction(const string& key) const {
        unsigned long hashVal = 0;
        for (char c : key) {
            hashVal = hashVal * 31 + static_cast<unsigned char>(c);
        }
        return static_cast<int>(hashVal % static_cast<unsigned long>(size));
    }

    /**
     * @brief Inserta un registro usando sondeo lineal.
     *
     * Si la posición inicial está ocupada, avanza secuencialmente
     * hasta encontrar una posición libre.
     *
     * @param key   Clave del registro.
     * @param value Valor asociado.
     */
    void insert(const string& key, const string& value) {
        int index = hashFunction(key);

        while (occupied[index]) {
            collisions++;
            index = (index + 1) % size;
        }

        table[index] = {key, value};
        occupied[index] = true;
    }

    /**
     * @brief Busca un registro por su clave usando sondeo lineal.
     *
     * @param  key Clave a buscar.
     * @return Valor asociado si se encontró, "No encontrado" en caso contrario.
     */
    string search(const string& key) const {
        int index = hashFunction(key);
        int start = index;

        while (occupied[index]) {
            if (table[index].key == key) {
                return table[index].value;
            }

            index = (index + 1) % size;

            // Evitar bucle infinito si la tabla está llena
            if (index == start) break;
        }

        return "No encontrado";
    }

    /** @return Número total de intentos fallidos de inserción. */
    int getCollisions() const { return collisions; }

    /**
     * @brief Calcula el factor de carga α = n / m.
     * @param  totalElements Número de elementos insertados.
     * @return Factor de carga como valor decimal.
     */
    double loadFactor(int totalElements) const {
        return static_cast<double>(totalElements) / size;
    }
};


// =============================================================================
// FUNCIÓN: Leer claves desde un archivo CSV
// =============================================================================

/**
 * @brief Lee las claves de la primera columna de un archivo CSV.
 *
 * Omite la fila de encabezado y lee hasta `limit` filas. Asume
 * que la primera columna contiene el user_id (o clave deseada).
 *
 * @param filename Ruta al archivo CSV.
 * @param limit    Número máximo de filas a leer.
 * @return Vector de strings con las claves extraídas.
 */
vector<string> readKeysFromCSV(const string& filename, int limit) {
    vector<string> keys;
    ifstream file(filename);

    if (!file.is_open()) {
        cerr << "\n  ERROR: No se pudo abrir '" << filename << "'.\n";
        cerr << "  Descarga el dataset desde:\n";
        cerr << "  https://www.kaggle.com/datasets/mkechinov/"
                "ecommerce-behavior-data-from-multi-category-store\n\n";
        return keys;
    }

    string line;
    getline(file, line);  // Omitir encabezado

    while (getline(file, line) && static_cast<int>(keys.size()) < limit) {
        stringstream ss(line);
        string column;
        vector<string> columns;

        while (getline(ss, column, ',')) {
            columns.push_back(column);
        }

        if (!columns.empty() && !columns[0].empty()) {
            keys.push_back(columns[0]);
        }
    }

    return keys;
}


// =============================================================================
// FUNCIÓN: Imprimir línea separadora
// =============================================================================

void printSeparator(char c = '-', int width = 60) {
    cout << string(width, c) << "\n";
}


// =============================================================================
// PROGRAMA PRINCIPAL
// =============================================================================

int main() {
    printSeparator('=');
    cout << "  ANÁLISIS DE TABLAS HASH - DATOS KAGGLE (C++)\n";
    printSeparator('=');

    // ------------------------------------------------------------------
    // Configuración del experimento
    // ------------------------------------------------------------------
    const string FILENAME   = "ecommerce_sample.csv";
    const int    LIMIT      = 10'000;
    const int    TABLE_SIZE = 20'011;  // Número primo
    const int    SEARCH_N   = 1'000;

    // ------------------------------------------------------------------
    // 1. Cargar claves desde el CSV
    // ------------------------------------------------------------------
    cout << "\n[1] Cargando dataset...\n";
    vector<string> keys = readKeysFromCSV(FILENAME, LIMIT);

    if (keys.empty()) return 1;

    cout << "  -> Claves cargadas: " << keys.size() << "\n";
    cout << "  -> Tamaño de tabla: " << TABLE_SIZE << "\n";

    // ------------------------------------------------------------------
    // 2. Prueba: Encadenamiento Separado
    // ------------------------------------------------------------------
    cout << "\n[2] Prueba con Encadenamiento Separado...\n";
    HashTableChaining hashChain(TABLE_SIZE);

    auto t0 = high_resolution_clock::now();
    for (const string& key : keys) {
        hashChain.insert(key, key);
    }
    auto t1 = high_resolution_clock::now();
    duration<double> insertChainTime = t1 - t0;

    t0 = high_resolution_clock::now();
    for (int i = 0; i < SEARCH_N && i < static_cast<int>(keys.size()); i++) {
        hashChain.search(keys[i]);
    }
    t1 = high_resolution_clock::now();
    duration<double> searchChainTime = t1 - t0;

    cout << fixed << setprecision(6);
    cout << "  -> Insercion:  " << insertChainTime.count() << " s\n";
    cout << "  -> Busqueda:   " << searchChainTime.count() << " s\n";
    cout << "  -> Colisiones: " << hashChain.getCollisions() << "\n";
    cout << "  -> Factor de carga: "
         << hashChain.loadFactor(static_cast<int>(keys.size())) << "\n";

    // ------------------------------------------------------------------
    // 3. Prueba: Sondeo Lineal
    // ------------------------------------------------------------------
    cout << "\n[3] Prueba con Sondeo Lineal...\n";
    HashTableLinear hashLinear(TABLE_SIZE);

    t0 = high_resolution_clock::now();
    for (const string& key : keys) {
        hashLinear.insert(key, key);
    }
    t1 = high_resolution_clock::now();
    duration<double> insertLinearTime = t1 - t0;

    t0 = high_resolution_clock::now();
    for (int i = 0; i < SEARCH_N && i < static_cast<int>(keys.size()); i++) {
        hashLinear.search(keys[i]);
    }
    t1 = high_resolution_clock::now();
    duration<double> searchLinearTime = t1 - t0;

    cout << "  -> Insercion:  " << insertLinearTime.count() << " s\n";
    cout << "  -> Busqueda:   " << searchLinearTime.count() << " s\n";
    cout << "  -> Colisiones: " << hashLinear.getCollisions() << "\n";
    cout << "  -> Factor de carga: "
         << hashLinear.loadFactor(static_cast<int>(keys.size())) << "\n";

    // ------------------------------------------------------------------
    // 4. Tabla resumen de resultados
    // ------------------------------------------------------------------
    cout << "\n[4] Resultados del experimento:\n";
    printSeparator();
    cout << left
         << setw(22) << "Metodo"
         << setw(16) << "Ins. (s)"
         << setw(16) << "Busq. (s)"
         << setw(14) << "Colisiones"
         << "Carga\n";
    printSeparator();
    cout << setw(22) << "Encadenamiento"
         << setw(16) << insertChainTime.count()
         << setw(16) << searchChainTime.count()
         << setw(14) << hashChain.getCollisions()
         << hashChain.loadFactor(static_cast<int>(keys.size())) << "\n";

    cout << setw(22) << "Sondeo Lineal"
         << setw(16) << insertLinearTime.count()
         << setw(16) << searchLinearTime.count()
         << setw(14) << hashLinear.getCollisions()
         << hashLinear.loadFactor(static_cast<int>(keys.size())) << "\n";
    printSeparator();

    cout << "\n";
    printSeparator('=');
    cout << "  Ejecucion completada exitosamente.\n";
    printSeparator('=');

    return 0;
}
