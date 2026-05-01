import time
import random
from typing import List

# ========== ALGORITMOS NO COMPARATIVOS ==========

# 1. COUNTING SORT
def counting_sort_full(arr: List[int], max_val: int = None) -> List[int]:
    """Algoritmo de ordenamiento no comparativo basado en conteo"""
    if not arr:
        return arr
    if max_val is None:
        max_val = max(arr)
    
    count = [0] * (max_val + 1)
    output = [0] * len(arr)
    
    for num in arr:
        count[num] += 1
    
    for i in range(1, max_val + 1):
        count[i] += count[i - 1]
    
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i]] - 1] = arr[i]
        count[arr[i]] -= 1
    
    return output

# 2. RADIX SORT (usando Counting Sort como subrutina)
def counting_sort_radix(arr: List[int], exp: int) -> None:
    """Counting sort para radix sort"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr: List[int]) -> List[int]:
    """Ordena usando Radix Sort (por dígitos)"""
    arr_copy = arr.copy()
    if not arr_copy:
        return arr_copy
    
    max_num = max(arr_copy)
    exp = 1
    
    while max_num // exp > 0:
        counting_sort_radix(arr_copy, exp)
        exp *= 10
    
    return arr_copy

# 3. BUCKET SORT
def bucket_sort(arr: List[float]) -> List[float]:
    """Ordena usando Bucket Sort (para números en [0, 1))"""
    if len(arr) == 0:
        return arr
    
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]
    
    # Distribuir elementos en cubetas
    for num in arr:
        index = int(bucket_count * num)
        if index == bucket_count:
            index -= 1
        buckets[index].append(num)
    
    # Ordenar cada cubeta e concatenar
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))
    
    return sorted_arr

# ========== ALGORITMOS COMPARATIVOS ==========

# 4. QUICK SORT
def quick_sort(arr: List[int]) -> List[int]:
    """Algoritmo comparativo: QuickSort"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# 5. MERGE SORT
def merge_sort(arr: List[int]) -> List[int]:
    """Algoritmo comparativo: MergeSort"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """Función auxiliar para MergeSort"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 6. TIMSORT (integrado en Python)
def timsort_python(arr: List[int]) -> List[int]:
    """Utiliza el sorted() de Python (que usa Timsort internamente)"""
    return sorted(arr)

# ========== FUNCIÓN DE COMPARACIÓN Y BENCHMARKING ==========

def benchmark_algorithm(algorithm, arr, algorithm_name):
    """Mide el tiempo de ejecución de un algoritmo"""
    arr_copy = arr.copy()
    
    start = time.time()
    result = algorithm(arr_copy)
    end = time.time()
    
    elapsed = (end - start) * 1000  # Convertir a milisegundos
    return elapsed, result

def run_benchmarks(n=100000):
    """Ejecuta benchmarks con n elementos aleatorios"""
    print(f"\n{'='*70}")
    print(f"BENCHMARK CON {n} NÚMEROS ALEATORIOS")
    print(f"{'='*70}\n")
    
    # Generar datos
    arr_random = [random.randint(0, 100000) for _ in range(n)]
    arr_small_range = [random.randint(0, 1000) for _ in range(n)]  # Rango pequeño
    arr_nearly_sorted = sorted(arr_random[:int(n*0.9)]) + arr_random[int(n*0.9):]  # Casi ordenado
    
    algorithms = [
        ("Counting Sort (rango 0-1000)", lambda x: counting_sort_full(x, 1000), arr_small_range),
        ("Radix Sort", radix_sort, arr_random),
        ("QuickSort", quick_sort, arr_random),
        ("MergeSort", merge_sort, arr_random),
        ("Timsort (sorted)", timsort_python, arr_random),
    ]
    
    print("1. ARREGLO CON VALORES ALEATORIOS (0-100,000):")
    print("-" * 70)
    times = []
    for name, algo, arr in algorithms[1:]:  # Excluir counting sort en este caso
        try:
            elapsed, _ = benchmark_algorithm(algo, arr, name)
            times.append((name, elapsed))
            print(f"{name:.<45} {elapsed:>10.4f} ms")
        except Exception as e:
            print(f"{name:.<45} ERROR: {str(e)[:30]}")
    
    print("\n2. ARREGLO CON RANGO PEQUEÑO (0-1000):")
    print("-" * 70)
    for name, algo, arr in algorithms[:1]:  # Solo Counting Sort
        elapsed, _ = benchmark_algorithm(algo, arr, name)
        print(f"{name:.<45} {elapsed:>10.4f} ms")
    
    for name, algo, arr in algorithms[1:]:  # Resto de algoritmos
        try:
            elapsed, _ = benchmark_algorithm(algo, arr[:n], name)
            print(f"{name:.<45} {elapsed:>10.4f} ms")
        except Exception as e:
            print(f"{name:.<45} ERROR: {str(e)[:30]}")
    
    print("\n3. ARREGLO CASI ORDENADO:")
    print("-" * 70)
    for name, algo, arr in algorithms[1:]:
        try:
            elapsed, _ = benchmark_algorithm(algo, arr_nearly_sorted, name)
            print(f"{name:.<45} {elapsed:>10.4f} ms")
        except Exception as e:
            print(f"{name:.<45} ERROR: {str(e)[:30]}")

# ========== PRUEBAS SIMPLES ==========

print("\n" + "="*70)
print("PRUEBAS SIMPLES DE FUNCIONAMIENTO")
print("="*70 + "\n")

# Prueba 1: Counting Sort
arr1 = [5, 2, 1, 7, 3, 2, 5, 0]
print(f"Original:       {arr1}")
print(f"Counting Sort:  {counting_sort_full(arr1.copy(), 7)}\n")

# Prueba 2: Radix Sort
arr2 = [329, 457, 657, 839, 436, 720, 355]
print(f"Original:       {arr2}")
print(f"Radix Sort:     {radix_sort(arr2.copy())}\n")

# Prueba 3: Bucket Sort (valores normalizados)
arr3 = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
print(f"Original:       {arr3}")
print(f"Bucket Sort:    {bucket_sort(arr3.copy())}\n")

# Prueba 4: Comparativa de algoritmos comparativos
arr4 = [329, 457, 657, 839, 436, 720, 355]
print(f"Original:       {arr4}")
print(f"QuickSort:      {quick_sort(arr4.copy())}")
print(f"MergeSort:      {merge_sort(arr4.copy())}")
print(f"Timsort:        {timsort_python(arr4.copy())}\n")

# ========== BENCHMARKING ==========

# Ejecutar benchmarks con diferentes tamaños
run_benchmarks(10000)
run_benchmarks(100000)
