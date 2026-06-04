<<<<<<< HEAD
#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>   // Para std::swap
#include <random>      // Para generacion de datos aleatorios
using namespace std;
using namespace std::chrono;

// Contadores globales de operaciones
long long comparaciones = 0, intercambios = 0;

// BUBBLE SORT
// Recorre repetidamente el arreglo comparando elementos adyacentes.
// Complejidad: O(n2) promedio y peor caso; O(n) mejor caso con bandera.
void bubbleSort(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n - 1; i++) {
        bool intercambio = false;
        for (int j = 0; j < n - i - 1; j++) {
            comparaciones++;
            if (a[j] > a[j+1]) {
                swap(a[j], a[j+1]);
                intercambios++;
                intercambio = true;
            }
        }
        if (!intercambio) break;
    }
}

// INSERTION SORT
// Construye la secuencia ordenada insertando cada nuevo elemento
// en su posicion correcta dentro del subarreglo ya ordenado.
void insertionSort(vector<int>& a) {
    int n = a.size();
    for (int i = 1; i < n; i++) {
        int clave = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > clave) {
            comparaciones++;
            a[j+1] = a[j];
            intercambios++;
            j--;
        }
        comparaciones++;
        a[j+1] = clave;
    }
}

// MERGE SORT
void merge(vector<int>& a, int ini, int mid, int fin) {
    vector<int> izq(a.begin()+ini, a.begin()+mid+1);
    vector<int> der(a.begin()+mid+1, a.begin()+fin+1);
    int i=0, j=0, k=ini;
    while (i<(int)izq.size() && j<(int)der.size()) {
        comparaciones++;
        if (izq[i] <= der[j]) a[k++] = izq[i++];
        else                  a[k++] = der[j++];
        intercambios++;
    }
    while (i<(int)izq.size()) { a[k++]=izq[i++]; intercambios++; }
    while (j<(int)der.size()) { a[k++]=der[j++]; intercambios++; }
}
void mergeSort(vector<int>& a, int ini, int fin) {
    if (ini >= fin) return;
    int mid = (ini + fin) / 2;
    mergeSort(a, ini, mid);
    mergeSort(a, mid+1, fin);
    merge(a, ini, mid, fin);
}

// QUICK SORT
int particion(vector<int>& a, int ini, int fin) {
    int pivote = a[fin];
    int i = ini - 1;
    for (int j = ini; j < fin; j++) {
        comparaciones++;
        if (a[j] <= pivote) {
            i++;
            swap(a[i], a[j]);
            intercambios++;
        }
    }
    swap(a[i+1], a[fin]);
    intercambios++;
    return i + 1;
}
void quickSort(vector<int>& a, int ini, int fin) {
    if (ini < fin) {
        int p = particion(a, ini, fin);
        quickSort(a, ini, p-1);
        quickSort(a, p+1, fin);
    }
}

// Funcion de medicion
void medir(vector<int> arr, void(*fn)(vector<int>&), const string& nombre) {
    comparaciones = intercambios = 0;
    auto t0 = high_resolution_clock::now();
    fn(arr);
    auto t1 = high_resolution_clock::now();
    double ms = duration<double,milli>(t1-t0).count();
    cout << nombre << " | Tiempo: " << ms << " ms"
         << " | Comp: "  << comparaciones
         << " | Interc: " << intercambios << endl;
}

int main() {
    int N = 1000;
    vector<int> aleatorio(N);
    mt19937 rng(42);
    generate(aleatorio.begin(), aleatorio.end(), [&](){ return rng()%10000; });
    vector<int> ordenado = aleatorio;
    sort(ordenado.begin(), ordenado.end());
    vector<int> inverso(ordenado.rbegin(), ordenado.rend());

    for (auto& [nombre, entrada] : vector<pair<string,vector<int>>>{
        {"Aleatorio", aleatorio}, {"Ordenado", ordenado}, {"Inverso", inverso}}) {
        cout << "=== " << nombre << " ===" << endl;
        medir(entrada, bubbleSort,    "Bubble Sort   ");
        medir(entrada, insertionSort, "Insertion Sort");
        auto ms = [](vector<int>& a){ mergeSort(a,0,a.size()-1); };
        medir(entrada, ms,            "Merge Sort    ");
        auto qs = [](vector<int>& a){ quickSort(a,0,a.size()-1); };
        medir(entrada, qs,            "Quick Sort    ");
    }
    return 0;
}
=======
#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>   // Para std::swap
#include <random>      // Para generacion de datos aleatorios
using namespace std;
using namespace std::chrono;

// Contadores globales de operaciones
long long comparaciones = 0, intercambios = 0;

// BUBBLE SORT
// Recorre repetidamente el arreglo comparando elementos adyacentes.
// Complejidad: O(n2) promedio y peor caso; O(n) mejor caso con bandera.
void bubbleSort(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n - 1; i++) {
        bool intercambio = false;
        for (int j = 0; j < n - i - 1; j++) {
            comparaciones++;
            if (a[j] > a[j+1]) {
                swap(a[j], a[j+1]);
                intercambios++;
                intercambio = true;
            }
        }
        if (!intercambio) break;
    }
}

// INSERTION SORT
// Construye la secuencia ordenada insertando cada nuevo elemento
// en su posicion correcta dentro del subarreglo ya ordenado.
void insertionSort(vector<int>& a) {
    int n = a.size();
    for (int i = 1; i < n; i++) {
        int clave = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > clave) {
            comparaciones++;
            a[j+1] = a[j];
            intercambios++;
            j--;
        }
        comparaciones++;
        a[j+1] = clave;
    }
}

// MERGE SORT
void merge(vector<int>& a, int ini, int mid, int fin) {
    vector<int> izq(a.begin()+ini, a.begin()+mid+1);
    vector<int> der(a.begin()+mid+1, a.begin()+fin+1);
    int i=0, j=0, k=ini;
    while (i<(int)izq.size() && j<(int)der.size()) {
        comparaciones++;
        if (izq[i] <= der[j]) a[k++] = izq[i++];
        else                  a[k++] = der[j++];
        intercambios++;
    }
    while (i<(int)izq.size()) { a[k++]=izq[i++]; intercambios++; }
    while (j<(int)der.size()) { a[k++]=der[j++]; intercambios++; }
}
void mergeSort(vector<int>& a, int ini, int fin) {
    if (ini >= fin) return;
    int mid = (ini + fin) / 2;
    mergeSort(a, ini, mid);
    mergeSort(a, mid+1, fin);
    merge(a, ini, mid, fin);
}

// QUICK SORT
int particion(vector<int>& a, int ini, int fin) {
    int pivote = a[fin];
    int i = ini - 1;
    for (int j = ini; j < fin; j++) {
        comparaciones++;
        if (a[j] <= pivote) {
            i++;
            swap(a[i], a[j]);
            intercambios++;
        }
    }
    swap(a[i+1], a[fin]);
    intercambios++;
    return i + 1;
}
void quickSort(vector<int>& a, int ini, int fin) {
    if (ini < fin) {
        int p = particion(a, ini, fin);
        quickSort(a, ini, p-1);
        quickSort(a, p+1, fin);
    }
}

// Funcion de medicion
void medir(vector<int> arr, void(*fn)(vector<int>&), const string& nombre) {
    comparaciones = intercambios = 0;
    auto t0 = high_resolution_clock::now();
    fn(arr);
    auto t1 = high_resolution_clock::now();
    double ms = duration<double,milli>(t1-t0).count();
    cout << nombre << " | Tiempo: " << ms << " ms"
         << " | Comp: "  << comparaciones
         << " | Interc: " << intercambios << endl;
}

int main() {
    int N = 1000;
    vector<int> aleatorio(N);
    mt19937 rng(42);
    generate(aleatorio.begin(), aleatorio.end(), [&](){ return rng()%10000; });
    vector<int> ordenado = aleatorio;
    sort(ordenado.begin(), ordenado.end());
    vector<int> inverso(ordenado.rbegin(), ordenado.rend());

    for (auto& [nombre, entrada] : vector<pair<string,vector<int>>>{
        {"Aleatorio", aleatorio}, {"Ordenado", ordenado}, {"Inverso", inverso}}) {
        cout << "=== " << nombre << " ===" << endl;
        medir(entrada, bubbleSort,    "Bubble Sort   ");
        medir(entrada, insertionSort, "Insertion Sort");
        auto ms = [](vector<int>& a){ mergeSort(a,0,a.size()-1); };
        medir(entrada, ms,            "Merge Sort    ");
        auto qs = [](vector<int>& a){ quickSort(a,0,a.size()-1); };
        medir(entrada, qs,            "Quick Sort    ");
    }
    return 0;
}
>>>>>>> 1fffc74ac1891372de17add1d20a94fdf8a7fb3e
