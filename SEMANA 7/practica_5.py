import time
import random

# BUBBLE SORT
def bubble_sort(arr):
    a = arr[:]
    n, comp, interc = len(a), 0, 0
    for i in range(n - 1):
        intercambio = False
        for j in range(n - i - 1):
            comp += 1
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                interc += 1
                intercambio = True
        if not intercambio: break
    return a, comp, interc

# INSERTION SORT
def insertion_sort(arr):
    a = arr[:]
    comp, interc = 0, 0
    for i in range(1, len(a)):
        clave = a[i]
        j = i - 1
        while j >= 0 and a[j] > clave:
            comp += 1
            a[j+1] = a[j]
            interc += 1
            j -= 1
        comp += 1
        a[j+1] = clave
    return a, comp, interc

# MERGE SORT
def merge_sort(arr):
    comp = [0]; interc = [0]
    def _merge(a, ini, mid, fin):
        izq = a[ini:mid+1]
        der = a[mid+1:fin+1]
        i = j = 0; k = ini
        while i < len(izq) and j < len(der):
            comp[0] += 1
            if izq[i] <= der[j]: a[k] = izq[i]; i += 1
            else:                a[k] = der[j]; j += 1
            interc[0] += 1; k += 1
        while i < len(izq): a[k] = izq[i]; i+=1; k+=1; interc[0]+=1
        while j < len(der): a[k] = der[j]; j+=1; k+=1; interc[0]+=1
    def _ms(a, ini, fin):
        if ini >= fin: return
        mid = (ini + fin) // 2
        _ms(a, ini, mid); _ms(a, mid+1, fin)
        _merge(a, ini, mid, fin)
    a = arr[:]
    _ms(a, 0, len(a)-1)
    return a, comp[0], interc[0]

# QUICK SORT
def quick_sort(arr):
    comp = [0]; interc = [0]
    def _particion(a, ini, fin):
        pivote = a[fin]
        i = ini - 1
        for j in range(ini, fin):
            comp[0] += 1
            if a[j] <= pivote:
                i += 1
                a[i], a[j] = a[j], a[i]
                interc[0] += 1
        a[i+1], a[fin] = a[fin], a[i+1]
        interc[0] += 1
        return i + 1
    def _qs(a, ini, fin):
        if ini < fin:
            p = _particion(a, ini, fin)
            _qs(a, ini, p-1); _qs(a, p+1, fin)
    a = arr[:]
    _qs(a, 0, len(a)-1)
    return a, comp[0], interc[0]

# Funcion de medicion
def medir(nombre, fn, entrada):
    t0 = time.perf_counter()
    _, comp, interc = fn(entrada)
    t1 = time.perf_counter()
    print(f"{nombre} | Tiempo: {(t1-t0)*1000:.3f} ms"
          f" | Comp: {comp} | Interc: {interc}")

if __name__ == "__main__":
    N = 1000
    random.seed(42)
    aleatorio = [random.randint(0, 9999) for _ in range(N)]
    ordenado  = sorted(aleatorio)
    inverso   = sorted(aleatorio, reverse=True)

    for nombre_e, entrada in [("Aleatorio",aleatorio),("Ordenado",ordenado),("Inverso",inverso)]:
        print(f"=== {nombre_e} ===")
        medir("Bubble Sort   ", bubble_sort,    entrada)
        medir("Insertion Sort", insertion_sort, entrada)
        medir("Merge Sort    ", merge_sort,     entrada)
        medir("Quick Sort    ", quick_sort,     entrada)
