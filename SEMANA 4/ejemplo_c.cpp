#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include <iomanip>

using namespace std;

// ========== ALGORITMOS NO COMPARATIVOS ==========

// 1. COUNTING SORT
void countingSort(vector<int>& arr, int maxVal) {
    vector<int> count(maxVal + 1, 0);
    vector<int> output(arr.size());
    
    for (int num : arr) count[num]++;
    for (int i = 1; i <= maxVal; i++) count[i] += count[i - 1];
    for (int i = arr.size() - 1; i >= 0; i--) {
        output[count[arr[i]] - 1] = arr[i];
        count[arr[i]]--;
    }
    arr = output;
}

// 2. RADIX SORT (usando Counting Sort como subrutina)
void countingSortRadix(vector<int>& arr, int exp) {
    int n = arr.size();
    vector<int> output(n);
    vector<int> count(10, 0);
    
    for (int i = 0; i < n; i++) {
        int index = (arr[i] / exp) % 10;
        count[index]++;
    }
    
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }
    
    for (int i = n - 1; i >= 0; i--) {
        int index = (arr[i] / exp) % 10;
        output[count[index] - 1] = arr[i];
        count[index]--;
    }
    
    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
    }
}

void radixSort(vector<int>& arr) {
    if (arr.empty()) return;
    
    int maxNum = *max_element(arr.begin(), arr.end());
    
    for (int exp = 1; maxNum / exp > 0; exp *= 10) {
        countingSortRadix(arr, exp);
    }
}

// 3. BUCKET SORT
void bucketSort(vector<int>& arr, int maxVal) {
    if (arr.empty()) return;
    
    int bucketCount = arr.size();
    vector<vector<int>> buckets(bucketCount);
    
    // Distribuir elementos en cubetas
    for (int num : arr) {
        int index = (num * bucketCount) / (maxVal + 1);
        if (index >= bucketCount) index = bucketCount - 1;
        buckets[index].push_back(num);
    }
    
    // Ordenar cada cubeta usando insertion sort
    for (auto& bucket : buckets) {
        for (int i = 1; i < bucket.size(); i++) {
            int key = bucket[i];
            int j = i - 1;
            while (j >= 0 && bucket[j] > key) {
                bucket[j + 1] = bucket[j];
                j--;
            }
            bucket[j + 1] = key;
        }
    }
    
    // Concatenar
    int index = 0;
    for (auto& bucket : buckets) {
        for (int num : bucket) {
            arr[index++] = num;
        }
    }
}

// ========== ALGORITMOS COMPARATIVOS ==========

// 4. QUICK SORT
void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                swap(arr[i], arr[j]);
            }
        }
        swap(arr[i + 1], arr[high]);
        int pi = i + 1;
        
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void quickSortWrapper(vector<int>& arr) {
    if (!arr.empty()) {
        quickSort(arr, 0, arr.size() - 1);
    }
}

// 5. MERGE SORT
void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    
    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }
    
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    
    for (int i = 0; i < k; i++) {
        arr[left + i] = temp[i];
    }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

void mergeSortWrapper(vector<int>& arr) {
    if (!arr.empty()) {
        mergeSort(arr, 0, arr.size() - 1);
    }
}

// ========== FUNCIÓN DE BENCHMARK ==========

double benchmark(void (*sortFunc)(vector<int>&), vector<int> arr, const string& name) {
    clock_t start = clock();
    sortFunc(arr);
    clock_t end = clock();
    
    double elapsed = double(end - start) / CLOCKS_PER_SEC * 1000;  // ms
    return elapsed;
}

void printArray(const vector<int>& arr, const string& label, int limit = 10) {
    cout << label << ": ";
    for (int i = 0; i < min((int)arr.size(), limit); i++) {
        cout << arr[i] << " ";
    }
    if (arr.size() > limit) cout << "...";
    cout << endl;
}

// ========== MAIN ==========

int main() {
    cout << fixed << setprecision(4);
    
    cout << "\n" << string(70, '=') << endl;
    cout << "PRUEBAS SIMPLES DE FUNCIONAMIENTO" << endl;
    cout << string(70, '=') << "\n" << endl;
    
    // Prueba 1: Counting Sort
    vector<int> arr1 = {5, 2, 1, 7, 3, 2, 5, 0};
    vector<int> arr1_copy = arr1;
    countingSort(arr1_copy, 7);
    printArray(arr1, "Original");
    printArray(arr1_copy, "Counting Sort");
    cout << endl;
    
    // Prueba 2: Radix Sort
    vector<int> arr2 = {329, 457, 657, 839, 436, 720, 355};
    vector<int> arr2_copy = arr2;
    radixSort(arr2_copy);
    printArray(arr2, "Original");
    printArray(arr2_copy, "Radix Sort");
    cout << endl;
    
    // Prueba 3: Bucket Sort
    vector<int> arr3 = {5, 2, 1, 7, 3, 2, 5, 0};
    vector<int> arr3_copy = arr3;
    bucketSort(arr3_copy, 7);
    printArray(arr3, "Original");
    printArray(arr3_copy, "Bucket Sort");
    cout << endl;
    
    // Prueba 4: QuickSort
    vector<int> arr4 = {329, 457, 657, 839, 436, 720, 355};
    vector<int> arr4_copy = arr4;
    quickSortWrapper(arr4_copy);
    printArray(arr4, "Original");
    printArray(arr4_copy, "QuickSort");
    cout << endl;
    
    // Prueba 5: MergeSort
    vector<int> arr5 = {329, 457, 657, 839, 436, 720, 355};
    vector<int> arr5_copy = arr5;
    mergeSortWrapper(arr5_copy);
    printArray(arr5, "Original");
    printArray(arr5_copy, "MergeSort");
    cout << endl;
    
    // ========== BENCHMARKS ==========
    
    cout << string(70, '=') << endl;
    cout << "BENCHMARK CON 100,000 NÚMEROS ALEATORIOS" << endl;
    cout << string(70, '\n') << endl;
    
    int n = 100000;
    vector<int> arr_random(n);
    vector<int> arr_small_range(n);
    
    // Generar datos
    srand(time(0));
    for (int i = 0; i < n; i++) {
        arr_random[i] = rand() % 100001;
        arr_small_range[i] = rand() % 1001;
    }
    
    cout << "1. ARREGLO CON RANGO PEQUEÑO (0-1000):" << endl;
    cout << string(70, '-') << endl;
    {
        vector<int> test = arr_small_range;
        double time_cs = benchmark(
            [](vector<int>& arr) { countingSort(arr, 1000); },
            test,
            "Counting Sort"
        );
        cout << "Counting Sort..................... " << setw(10) << time_cs << " ms" << endl;
    }
    
    cout << "\n2. ARREGLO CON VALORES ALEATORIOS (0-100,000):" << endl;
    cout << string(70, '-') << endl;
    {
        vector<int> test = arr_random;
        double time_rs = benchmark(radixSort, test, "Radix Sort");
        cout << "Radix Sort........................ " << setw(10) << time_rs << " ms" << endl;
    }
    {
        vector<int> test = arr_random;
        double time_bs = benchmark(
            [](vector<int>& arr) { bucketSort(arr, 100000); },
            test,
            "Bucket Sort"
        );
        cout << "Bucket Sort....................... " << setw(10) << time_bs << " ms" << endl;
    }
    {
        vector<int> test = arr_random;
        double time_qs = benchmark(quickSortWrapper, test, "QuickSort");
        cout << "QuickSort......................... " << setw(10) << time_qs << " ms" << endl;
    }
    {
        vector<int> test = arr_random;
        double time_ms = benchmark(mergeSortWrapper, test, "MergeSort");
        cout << "MergeSort......................... " << setw(10) << time_ms << " ms" << endl;
    }
    
    cout << "\n" << string(70, '=') << endl;
    
    return 0;
}
