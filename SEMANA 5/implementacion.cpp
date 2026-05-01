// PRÁCTICA: TABLAS HASH EN C++
// Curso: Estructuras de Datos | Semanas 5-6

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <list>
#include <chrono>
#include <iomanip>
using namespace std;
using namespace std::chrono;

// ESTRUCTURA: Registro de datos del CSV

struct Registro {
    string clave;     // Campo usado como clave hash (ej: user_id)
    string valor;     // Campo auxiliar (ej: nombre, email)
};

// FUNCIÓN HASH PERSONALIZADA (Polinomial)
// h(k) = Σ(k[i] * 31^i) mod m

size_t funcionHash(const string& clave, size_t tamanio) {
    size_t hash = 0;                               //Valor hash inicial
    for (char c : clave) {                         //Itera cada caracter
        hash = (hash * 31 + (size_t)c) % tamanio;  // Acumula
    }
    return hash;                                   //Retorna indice
}

// CLASE: Tabla Hash con Encadenamiento Separado
// Cada celda contiene una lista enlazada de registros

class TablaHashEncadenamiento {
public:
    size_t tamanio;                    //numeri de cubos
    vector<list<Registro>> tabla;      // Vector de listas enlazadas
    long long colisiones = 0;          //Contador de colisiones
    long long elementos = 0;           //elementos insertados

    TablaHashEncadenamiento(size_t m) : tamanio(m), tabla(m) {}

    void insertar(const Registro& reg) {
        size_t idx = funcionHash(reg.clave, tamanio);  // Calcula índice
        if (!tabla[idx].empty())                       //Si no esta vacio
            colisiones++;                               // Registra colisión
        tabla[idx].push_back(reg);                     //Agrega al frente
        elementos++;
    }

    Registro* buscar(const string& clave) {
        size_t idx = funcionHash(clave, tamanio);     // Índice de la clave
        for (auto& reg : tabla[idx]) {                // recorre la cadena
            if (reg.clave == clave) return &reg;      // Si coincide, retorna
        }
        return nullptr;                                // No encontrado
    }

    double factorDeCarga() const {
        return (double)elementos / tamanio;            // λ = n / m
    }
};

// CLASE: Tabla Hash con Sondeo Lineal
// Direccionamiento abierto: h(k,i) = (h(k) + i) mod m

class TablaHashSondeoLineal {
    enum Estado { VACIO, OCUPADO, ELIMINADO };      // Estado de cada celda

public:
    size_t tamanio;
    vector<Registro> tabla;                        // arreglo de registros
    vector<Estado>   estados;                      // estado de cada celda
    long long colisiones = 0;
    long long elementos = 0;

    TablaHashSondeoLineal(size_t m)
        : tamanio(m), tabla(m), estados(m, VACIO) {}

    bool insertar(const Registro& reg) {
        if ((double)elementos / tamanio >= 0.75)     // Umbral de carga
            return false;                              // Tabla saturada
        size_t idx = funcionHash(reg.clave, tamanio); // Índice inicial
        size_t pasos = 0;
        while (estados[idx] == OCUPADO) {            // Mientras hay colisión
            colisiones++;                              // Cuenta colisión
            idx = (idx + 1) % tamanio;                 // sonda siguiente celda
            if (++pasos >=tamanio) return false;             // evita ciclo infinito
        }
        tabla[idx] = reg;                             // Inserta registro
        estados[idx] = OCUPADO;                       // Marca como ocupado
        elementos++;
        return true;
    }

    Registro* buscar(const string& clave) {
        size_t idx = funcionHash(clave, tamanio);
        size_t pasos = 0;
        while (estados[idx] != VACIO) {               // mientras no este vacio
            if (estados[idx] == OCUPADO && tabla[idx].clave == clave)
                return &tabla[idx];                   // Encontrado
            idx = (idx + 1) % tamanio;   
            if (++pasos >= tamanio) break;             // Encadena búsqueda
        }
        return nullptr;                               // No encontrado
    }
};

// LECTURA DE CSV

vector<Registro> leerCSV(const string& ruta, int col_clave, int col_valor) {
    vector<Registro> registros;
    ifstream archivo(ruta);                           // abre el archivo
    if (!archivo.is_open()) {
        cerr << "Error: no se pudo abrir " << ruta << endl;
        return registros;
    }

    string linea;
    getline(archivo, linea);                         // Salta encabezado
    while (getline(archivo, linea)) {                // lee linea por linea
        stringstream ss(linea);
        string campo;
        vector<string> campos;
        while (getline(ss, campo, ','))               // Divide por coma
            campos.push_back(campo);
        if ((int)campos.size() > max(col_clave, col_valor)) {
            Registro r;
            r.clave = campos[col_clave];              // Extrae clave
            r.valor = campos[col_valor];              // Extrae valor
            if (!r.clave.empty())                     // solo si la clave es valida
                registros.push_back(r);
        }
    }
    archivo.close();
    return registros;
}

// BENCHMARK Y COMPARACIÓN

void benchmark(const vector<Registro>& datos, vector<size_t> tamanios) {
    cout << left
        << setw(8) << "m"
        << setw(8) << "n"
        << setw(10) << "Col_Enc"
        << setw(12) << "Ins_enc(us)"
        << setw(10) << "Col_SL"
        << setw(12) << "Ins_SL(us)" << endl;
    cout << string(60, '-') << endl;

    for (size_t m : tamanios) {
        size_t n = min(datos.size(), (size_t)(m * 0.65)); // 65% de llenado

        // --- Encadenamiento ---
        TablaHashEncadenamiento th_enc(m);
        auto t0 = high_resolution_clock::now();
        for (size_t i = 0; i < n; i++) th_enc.insertar(datos[i]);
        auto t1 = high_resolution_clock::now();
        auto dur_enc = duration_cast<microseconds>(t1-t0).count();

        // --- Sondeo Lineal ---
        TablaHashSondeoLineal th_sl(m);
        t0 = high_resolution_clock::now();
        for (size_t i = 0; i < n; i++) th_sl.insertar(datos[i]);
        t1 = high_resolution_clock::now();
        auto dur_sl = duration_cast<microseconds>(t1-t0).count();

        cout << left
            << setw(8) << m
            << setw(8) << n
            << setw(10) << th_enc.colisiones
            << setw(12) << dur_enc
            << setw(10) << th_sl.colisiones
            << setw(12) << dur_sl << endl;
    }
}

// FUNCIÓN PRINCIPAL

int main() {
    cout << "=== BENCHMARK TABLAS HASH (C++) ===" << endl;

    // Cargar datos del archivo CSV
    vector<Registro> datos = leerCSV("D:/INGENIERIA DE SISTEMAS/5to SEMESTRE/ALGORITMOS Y ESTRUCTURAS DE DATOS/SEMANA 5/data usada/data.csv", 0, 1);
    
    // Si el archivo no se carga, usar datos sintéticos
    if (datos.empty()) {
        cout << "Usando datos sintéticos..." << endl;
    for (int i = 0; i < 5000; i++) {
        Registro r;
        r.clave = "reg_" + to_string(i+1);            // Genera claves unicas
        r.valor = "registro " + to_string(i);
        datos.push_back(r);
    }
    }

    cout << "Registros generados: " << datos.size() << endl << endl;

    vector<size_t> tamanios = {1009, 2003, 4001, 8009};  // Primos
    benchmark(datos, tamanios);

    return 0;
}