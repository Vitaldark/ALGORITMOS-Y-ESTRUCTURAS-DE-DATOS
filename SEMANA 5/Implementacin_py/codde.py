# ================================================================
# PRÁCTICA: TABLAS HASH CON DATOS REALES DE KAGGLE
# Curso: Estructuras de Datos | Semanas 5-6
# ================================================================

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # fix Unicode Windows

import os
import pandas as pd
import time
import matplotlib.pyplot as plt
import random

# ───────────────────────────────────────────────────────────────
# 1. CARGA Y LIMPIEZA DE DATOS DESDE CSV
# ───────────────────────────────────────────────────────────────
def cargar_datos(ruta_csv: str, columna_clave: str) -> list:
    df = pd.read_csv(ruta_csv, low_memory=False, encoding='latin-1')
    df[columna_clave] = df[columna_clave].astype(str).str.strip()
    claves = df[columna_clave].tolist()
    print(f'Registros cargados: {len(claves)}')
    return claves

# ───────────────────────────────────────────────────────────────
# 2. FUNCIÓN HASH
# ───────────────────────────────────────────────────────────────
def funcion_hash(clave: str, tamanio: int) -> int:
    hash_val = 0
    for c in str(clave):
        hash_val = (hash_val * 31 + ord(c)) % tamanio
    return hash_val

# ───────────────────────────────────────────────────────────────
# 3. TABLA HASH CON ENCADENAMIENTO
# ───────────────────────────────────────────────────────────────
class TablaHashEncadenamiento:
    def __init__(self, tamanio: int):
        self.tamanio = tamanio
        self.tabla = [[] for _ in range(tamanio)]
        self.colisiones = 0
        self.elementos = 0

    def insertar(self, clave: str, valor=None):
        idx = funcion_hash(clave, self.tamanio)
        self.colisiones += len(self.tabla[idx])
        self.tabla[idx].append((clave, valor))
        self.elementos += 1

    def buscar(self, clave: str):
        idx = funcion_hash(clave, self.tamanio)
        for k, v in self.tabla[idx]:
            if k == clave:
                return v
        return None

    def factor_de_carga(self):
        return self.elementos / self.tamanio

# ───────────────────────────────────────────────────────────────
# 4. TABLA HASH CON SONDEO LINEAL
# ───────────────────────────────────────────────────────────────
class TablaHashSondeoLineal:
    ELIMINADO = '__ELIMINADO__'

    def __init__(self, tamanio: int):
        self.tamanio = tamanio
        self.tabla = [None] * tamanio
        self.colisiones = 0
        self.elementos = 0

    def insertar(self, clave: str, valor=None):
        if self.elementos >= self.tamanio * 0.75:
            raise OverflowError('Tabla llena')

        idx = funcion_hash(clave, self.tamanio)
        pasos = 0

        while self.tabla[idx] is not None and self.tabla[idx] != self.ELIMINADO:
            self.colisiones += 1
            idx = (idx + 1) % self.tamanio
            pasos += 1
            if pasos >= self.tamanio:
                raise OverflowError('No hay espacio')

        self.tabla[idx] = (clave, valor)
        self.elementos += 1

    def buscar(self, clave: str):
        idx = funcion_hash(clave, self.tamanio)
        pasos = 0

        while self.tabla[idx] is not None:
            if self.tabla[idx] != self.ELIMINADO and self.tabla[idx][0] == clave:
                return self.tabla[idx][1]
            idx = (idx + 1) % self.tamanio
            pasos += 1
            if pasos >= self.tamanio:
                break

        return None

    def factor_de_carga(self):
        return self.elementos / self.tamanio

# ───────────────────────────────────────────────────────────────
# 5. BENCHMARK
# ───────────────────────────────────────────────────────────────
def benchmark_completo(claves, tamanios=[1009, 2003, 4001, 8009]):
    resultados = []

    for m in tamanios:
        subclaves = claves[:int(m * 0.65)]

        # Encadenamiento
        th_enc = TablaHashEncadenamiento(m)
        t0 = time.perf_counter()
        for c in subclaves:
            th_enc.insertar(c)
        t_ins_enc = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        for c in subclaves[:100]:
            th_enc.buscar(c)
        t_bus_enc = (time.perf_counter() - t0) * 1000

        # Sondeo lineal
        th_sl = TablaHashSondeoLineal(m)
        t0 = time.perf_counter()
        for c in subclaves:
            try:
                th_sl.insertar(c)
            except OverflowError:
                break
        t_ins_sl = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        for c in subclaves[:100]:
            th_sl.buscar(c)
        t_bus_sl = (time.perf_counter() - t0) * 1000

        # Python dict
        dict_py = {}
        t0 = time.perf_counter()
        for c in subclaves:
            dict_py[c] = None
        t_ins_py = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        for c in subclaves[:100]:
            dict_py.get(c)
        t_bus_py = (time.perf_counter() - t0) * 1000

        resultados.append({
            'tamanio': m,
            'n': len(subclaves),
            'lambda_enc': round(th_enc.factor_de_carga(), 3),
            'col_enc': th_enc.colisiones,
            'col_sl': th_sl.colisiones,
            'ins_enc_ms': round(t_ins_enc, 3),
            'bus_enc_ms': round(t_bus_enc, 3),
            'ins_sl_ms': round(t_ins_sl, 3),
            'bus_sl_ms': round(t_bus_sl, 3),
            'ins_py_ms': round(t_ins_py, 3),
            'bus_py_ms': round(t_bus_py, 3),
        })

        print(f'm={m} | col_enc={th_enc.colisiones} | col_sl={th_sl.colisiones}')

    return resultados

# ───────────────────────────────────────────────────────────────
# 6. TABLA
# ───────────────────────────────────────────────────────────────
def mostrar_tabla(resultados):
    print('\n' + '='*105)
    print(f'{"m":>6} {"n":>6} {"lambda":>8} {"ColEnc":>8} {"InsEnc":>10} {"BusEnc":>10} {"ColSL":>8} {"InsSL":>10} {"BusSL":>10} {"InsPy":>10}')
    print('='*105)

    for r in resultados:
        print(f'{r["tamanio"]:>6} {r["n"]:>6} {r["lambda_enc"]:>8} {r["col_enc"]:>8} {r["ins_enc_ms"]:>10} {r["bus_enc_ms"]:>10} {r["col_sl"]:>8} {r["ins_sl_ms"]:>10} {r["bus_sl_ms"]:>10} {r["ins_py_ms"]:>10}')

# ───────────────────────────────────────────────────────────────
# 7. GRÁFICOS
# ───────────────────────────────────────────────────────────────
def graficar_resultados(resultados):
    tamanios = [r['tamanio'] for r in resultados]
    col_enc  = [r['col_enc'] for r in resultados]
    col_sl   = [r['col_sl']  for r in resultados]
    ins_enc  = [r['ins_enc_ms'] for r in resultados]
    ins_sl   = [r['ins_sl_ms']  for r in resultados]
    ins_py   = [r['ins_py_ms']  for r in resultados]

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    axs[0].plot(tamanios, col_enc, marker='o', label='Encadenamiento')
    axs[0].plot(tamanios, col_sl,  marker='s', label='Sondeo Lineal')
    axs[0].set_title('Colisiones por tamaño de tabla')
    axs[0].set_xlabel('Tamaño m')
    axs[0].set_ylabel('Colisiones')
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(tamanios, ins_enc, marker='o', label='Encadenamiento')
    axs[1].plot(tamanios, ins_sl,  marker='s', label='Sondeo Lineal')
    axs[1].plot(tamanios, ins_py,  marker='^', label='Python dict')
    axs[1].set_title('Tiempo de Inserción (ms)')
    axs[1].set_xlabel('Tamaño m')
    axs[1].set_ylabel('Tiempo (ms)')
    axs[1].legend()
    axs[1].grid()

    plt.tight_layout()
    plt.savefig('resultados_hash.png', dpi=150)
    print('\nGrafico guardado como resultados_hash.png')
    plt.show()

# ───────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────
if __name__ == '__main__':

    # Ruta base del script
    base = os.path.dirname(os.path.abspath(__file__))

    # Diagnóstico: muestra dónde busca
    print('=== DIAGNÓSTICO DE RUTAS ===')
    print(f'Script en: {base}')

    posibles_rutas = [
        os.path.join(base, 'data.csv'),
        os.path.join(base, '..', 'data usada', 'data.csv'),
        os.path.join(base, '..', 'data.csv'),
        # Ruta absoluta de respaldo — ajusta si tu disco no es D:
        r'D:\Quinto Semestre\Algoritmos\Nueva carpeta\ALGORITMOS-Y-ESTRUCTURAS-DE-DATOS\SEMANA 5\data usada\data.csv',
    ]

    ruta_csv = None
    for ruta in posibles_rutas:
        ruta_norm = os.path.normpath(ruta)
        existe = os.path.exists(ruta_norm)
        print(f'  {"[OK]" if existe else "[NO]"} {ruta_norm}')
        if existe and ruta_csv is None:
            ruta_csv = ruta_norm

    print('============================\n')

    if ruta_csv is None:
        print('CSV no encontrado. Usando datos aleatorios...')
        random.seed(42)
        claves = [f'INV_{random.randint(1, 99999):05d}' for _ in range(5000)]
        claves = list(set(claves))
    else:
        print(f'CSV encontrado: {ruta_csv}')
        claves = cargar_datos(ruta_csv, 'InvoiceNo')

    print(f'Total de claves: {len(claves)}\n')

    resultados = benchmark_completo(claves)
    mostrar_tabla(resultados)
    graficar_resultados(resultados)