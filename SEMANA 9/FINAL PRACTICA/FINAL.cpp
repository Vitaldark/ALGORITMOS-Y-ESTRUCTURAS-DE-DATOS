#include <iostream>
#include <vector>
#include <unordered_map>
#include <stack>
#include <queue>
#include <iomanip>
#include <string>
#include <utility>
#include <limits>

using namespace std;

struct Estudiante {
    string codigo;
    string nombre;
    float nota1;
    float nota2;
    float nota3;
    float promedio;
};

// Estructuras de almacenamiento global
vector<Estudiante> hoja;
unordered_map<string, int> indiceHash;
stack<vector<Estudiante>> historial;
queue<string> colaAtencion;

// Función en línea para cálculo aritmético eficiente
inline float calcularPromedio(float n1, float n2, float n3) {
    return (n1 + n2 + n3) / 3.0f;
}

// Reconstrucción del índice asociativo O(n)
void actualizarHash() {
    indiceHash.clear();
    for (size_t i = 0; i < hoja.size(); ++i) {
        indiceHash[hoja[i].codigo] = static_cast<int>(i);
    }
}

// Resguardo del estado actual previo a mutaciones
void guardarHistorial() {
    historial.push(hoja);
}

// Función auxiliar para validar la entrada de notas en el rango [0, 20]
float solicitarNota(const string& mensaje) {
    float nota;
    while (true) {
        cout << mensaje;
        if (cin >> nota && nota >= 0.0f && nota <= 20.0f) {
            return nota;
        }
        cout << "[ERROR] Nota invalida. Debe ser un valor numerico entre 0 y 20.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

void registrarEstudiante() {
    Estudiante e;
    cout << "\n--- REGISTRAR NUEVO ESTUDIANTE ---\n";
    cout << "Codigo unico: ";
    cin >> e.codigo;

    // Validación de clave primaria duplicada en tiempo O(1)
    if (indiceHash.find(e.codigo) != indiceHash.end()) {
        cout << "[ERROR] El codigo ingresado ya se encuentra registrado.\n";
        return;
    }

    // Limpieza del buffer para poder usar getline correctamente
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    
    cout << "Apellidos y Nombres: ";
    getline(cin, e.nombre);

    if (e.nombre.empty()) {
        cout << "[ERROR] El nombre no puede estar vacio.\n";
        return;
    }

    // Solicitud de notas con validación integrada
    e.nota1 = solicitarNota("Nota 1 (0-20): ");
    e.nota2 = solicitarNota("Nota 2 (0-20): ");
    e.nota3 = solicitarNota("Nota 3 (0-20): ");

    e.promedio = calcularPromedio(e.nota1, e.nota2, e.nota3);

    guardarHistorial();
    hoja.push_back(e);
    actualizarHash();
    cout << "[EXITO] Registro insertado e indexado correctamente.\n";
}

void mostrarHoja() {
    if (hoja.empty()) {
        cout << "\n[AVISO] La hoja de calculo no contiene registros.\n";
        return;
    }
    cout << "\n========================================================================\n";
    cout << "                     MINI HOJA DE CALCULO ACADEMICA                     \n";
    cout << "========================================================================\n";
    cout << left << setw(12) << "Codigo"
         << setw(30) << "Nombre Completo"
         << setw(8) << "N1"
         << setw(8) << "N2"
         << setw(8) << "N3"
         << setw(10) << "Promedio" << endl;
    cout << "------------------------------------------------------------------------\n";
    for (const auto &e : hoja) {
        cout << left << setw(12) << e.codigo
             << setw(30) << e.nombre
             << setw(8) << setprecision(1) << fixed << e.nota1
             << setw(8) << e.nota2
             << setw(8) << e.nota3
             << setw(10) << setprecision(2) << e.promedio << endl;
    }
    cout << "========================================================================\n";
}

void buscarEstudiante() {
    string codigo;
    cout << "\nIngrese el codigo a buscar en Tabla Hash: ";
    cin >> codigo;
    
    auto it = indiceHash.find(codigo);
    if (it != indiceHash.end()) {
        int pos = it->second;
        const auto &e = hoja[pos];
        cout << "\n[REGISTRO ENCONTRADO - BUSQUEDA O(1)]\n";
        cout << "Estudiante: " << e.nombre << " | Promedio Actual: " << fixed << setprecision(2) << e.promedio << "\n";
    } else {
        cout << "[AVISO] Codigo no registrado en la base indexada.\n";
    }
}

// QuickSort: Particionamiento por Promedio (Descendente de Mayor a Menor)
int particion(vector<Estudiante> &arr, int bajo, int alto) {
    float pivote = arr[alto].promedio;
    int i = bajo - 1;
    for (int j = bajo; j < alto; j++) {
        if (arr[j].promedio >= pivote) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[alto]);
    return i + 1;
}

void quickSort(vector<Estudiante> &arr, int bajo, int alto) {
    if (bajo < alto) {
        int pi = particion(arr, bajo, alto);
        quickSort(arr, bajo, pi - 1);
        quickSort(arr, pi + 1, alto);
    }
}

// MergeSort: Combinación por Código Alfanumérico (Ascendente)
void merge(vector<Estudiante> &arr, int izq, int medio, int der) {
    int n1 = medio - izq + 1;
    int n2 = der - medio;
    vector<Estudiante> L(n1), R(n2);
    for (int i = 0; i < n1; i++) L[i] = arr[izq + i];
    for (int j = 0; j < n2; j++) R[j] = arr[medio + 1 + j];
    
    int i = 0, j = 0, k = izq;
    while (i < n1 && j < n2) {
        if (L[i].codigo <= R[j].codigo) {
            arr[k] = L[i]; i++;
        } else {
            arr[k] = R[j]; j++;
        }
        k++;
    }
    while (i < n1) { arr[k] = L[i]; i++; k++; }
    while (j < n2) { arr[k] = R[j]; j++; k++; }
}

void mergeSort(vector<Estudiante> &arr, int izq, int der) {
    if (izq < der) {
        int medio = izq + (der - izq) / 2;
        mergeSort(arr, izq, medio);
        mergeSort(arr, medio + 1, der);
        merge(arr, izq, medio, der);
    }
}

void ordenarPorPromedio() {
    if (hoja.empty()) return;
    guardarHistorial();
    quickSort(hoja, 0, static_cast<int>(hoja.size() - 1));
    actualizarHash();
    cout << "[OK] Filas ordenadas por Promedio (Descendente) via QuickSort.\n";
}

void ordenarPorCodigo() {
    if (hoja.empty()) return;
    guardarHistorial();
    mergeSort(hoja, 0, static_cast<int>(hoja.size() - 1));
    actualizarHash();
    cout << "[OK] Filas ordenadas por Codigo (Ascendente) via MergeSort.\n";
}

void deshacer() {
    if (!historial.empty()) {
        hoja = historial.top();
        historial.pop();
        actualizarHash();
        cout << "[UNDO] Estado de celdas restaurado al punto de control anterior.\n";
    } else {
        cout << "[INFO] No existen acciones registradas para deshacer.\n";
    }
}

void agregarColaAtencion() {
    string codigo;
    cout << "\nIngrese el codigo del estudiante que entra a la cola: ";
    cin >> codigo;
    if (indiceHash.find(codigo) != indiceHash.end()) {
        colaAtencion.push(codigo);
        cout << "[COLA] Estudiante ingresado en la cola FIFO de secretaria.\n";
    } else {
        cout << "[ERROR] El codigo no figura registrado en la hoja actual.\n";
    }
}

void atenderEstudiante() {
    if (!colaAtencion.empty()) {
        string codigo = colaAtencion.front();
        colaAtencion.pop();
        
        // Verificación de seguridad por si el estudiante fue borrado mediante un "Deshacer"
        auto it = indiceHash.find(codigo);
        if (it != indiceHash.end()) {
            int pos = it->second;
            cout << "[ATENCION] Despachando requerimiento de: " << hoja[pos].nombre << "\n";
        } else {
            cout << "[AVISO] El estudiante en cola ya no se encuentra en los registros vigentes.\n";
        }
    } else {
        cout << "[INFO] Canal de atencion despejado. Cola vacia.\n";
    }
}

// Función Recursiva para acumulación de promedios.
// Se limita la recursión si el volumen supera el tamaño seguro de stack estándar (~5000 llamadas).
float sumaPromediosRecursiva(size_t i) {
    if (i == hoja.size()) return 0.0f;
    return hoja[i].promedio + sumaPromediosRecursiva(i + 1);
}

void estadisticas() {
    if (hoja.empty()) {
        cout << "\n[AVISO] Hoja sin datos para el calculo estadistico.\n";
        return;
    }
    
    float suma = 0.0f;
    // Si la hoja es inmensa, preferimos un enfoque iterativo para evitar Stack Overflow
    if (hoja.size() < 4000) {
        suma = sumaPromediosRecursiva(0);
    } else {
        for (const auto& e : hoja) suma += e.promedio;
    }
    
    float promedioGeneral = suma / static_cast<float>(hoja.size());
    
    // Analítica adicional de apoyo (Máximos y Mínimos)
    size_t posMejor = 0, posPeor = 0;
    for (size_t i = 1; i < hoja.size(); ++i) {
        if (hoja[i].promedio > hoja[posMejor].promedio) posMejor = i;
        if (hoja[i].promedio < hoja[posPeor].promedio) posPeor = i;
    }

    cout << "\n========= METRICAS ANALITICAS GENERALES =========\n";
    cout << " Estudiantes Procesados : " << hoja.size() << "\n";
    cout << " Promedio General Coho. : " << fixed << setprecision(2) << promedioGeneral << "\n";
    cout << " Rendimiento Mas Alto   : " << hoja[posMejor].promedio << " (" << hoja[posMejor].nombre << ")\n";
    cout << " Rendimiento Mas Bajo   : " << hoja[posPeor].promedio << " (" << hoja[posPeor].nombre << ")\n";
    cout << "=================================================\n";
}

void menu() {
    int opcion;
    do {
        cout << "\n=============================================\n";
        cout << "         MENU PRINCIPAL - SPREADSHEET        \n";
        cout << "=============================================\n";
        cout << "1. Registrar Estudiante (Fila)\n";
        cout << "2. Mostrar Hoja de Calculo\n";
        cout << "3. Buscar Estudiante por Codigo (Hash)\n";
        cout << "4. Ordenar por Promedio [QuickSort Desc]\n";
        cout << "5. Ordenar por Codigo [MergeSort Asc]\n";
        cout << "6. Deshacer Ultima Modificacion [Stack]\n";
        cout << "7. Insertar Estudiante a Cola de Atencion\n";
        cout << "8. Atender Siguiente Estudiante [FIFO]\n";
        cout << "9. Mostrar Estadisticas Consolidadas\n";
        cout << "10. Salir de la Aplicacion\n";
        cout << "---------------------------------------------\n";
        cout << "Seleccione una opcion (1-10): ";
        
        if (!(cin >> opcion)) {
            cout << "[ALERTA] Entrada invalida. Ingrese un numero.\n";
            cin.clear(); 
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); 
            continue;
        }
        
        switch (opcion) {
            case 1: registrarEstudiante(); break;
            case 2: mostrarHoja(); break;
            case 3: buscarEstudiante(); break;
            case 4: ordenarPorPromedio(); break;
            case 5: ordenarPorCodigo(); break;
            case 6: deshacer(); break;
            case 7: agregarColaAtencion(); break;
            case 8: atenderEstudiante(); break;
            case 9: estadisticas(); break;
            case 10: cout << "\nLiberando memoria interna... Programa cerrado.\n"; break;
            default: cout << "[ERROR] Opcion fuera de rango.\n";
        }
    } while (opcion != 10);
}

int main() {
    // Optimización de flujos estándar I/O de C++
   // ios_base::sync_with_stdio(false);
   // cin.tie(NULL);
    
    menu();
    return 0;
}