from collections import deque
from copy import deepcopy

# Estructuras de datos globales
hoja = []
indice_hash = {}
historial = []
cola_atencion = deque()

def calcular_promedio(n1, n2, n3):
    return (n1 + n2 + n3) / 3.0

def actualizar_hash():
    indice_hash.clear()
    for idx, estudiante in enumerate(hoja):
        indice_hash[estudiante["codigo"]] = idx

def guardar_historial():
    # Uso de deepcopy para aislar estados mutables dentro del Stack (Historial de cambios)
    historial.append(deepcopy(hoja))

def solicitar_nota(mensaje):
    """Solicita una nota por consola asegurando que esté entre 0 y 20."""
    while True:
        try:
            nota = float(input(mensaje))
            if 0 <= nota <= 20:
                return nota
            print("[ERROR] La calificación debe estar en el rango de 0 a 20.")
        except ValueError:
            print("[ERROR] Ingrese un valor numérico válido.")

def registrar_estudiante():
    print("\n--- REGISTRAR NUEVO ESTUDIANTE ---")
    codigo = input("Código único: ").strip()
    
    if not codigo:
        print("[ERROR] El código no puede estar vacío.")
        return
    if codigo in indice_hash:
        print("[ERROR] Llave primaria duplicada. El código ya existe.")
        return
        
    nombre = input("Apellidos y Nombres: ").strip()
    if not nombre:
        print("[ERROR] El nombre no puede estar vacío.")
        return

    # Validaciones de notas mejoradas
    nota1 = solicitar_nota("Nota 1 (0-20): ")
    nota2 = solicitar_nota("Nota 2 (0-20): ")
    nota3 = solicitar_nota("Nota 3 (0-20): ")
    
    estudiante = {
        "codigo": codigo,
        "nombre": nombre,
        "nota1": nota1,
        "nota2": nota2,
        "nota3": nota3,
        "promedio": round(calcular_promedio(nota1, nota2, nota3), 2)
    }
    
    guardar_historial()
    hoja.append(estudiante)
    actualizar_hash()
    print("[ÉXITO] Estudiante registrado e indexado correctamente.")

def mostrar_hoja():
    if not hoja:
        print("\n[AVISO] La hoja de cálculo no contiene registros activos.")
        return
    
    print("\n" + "="*75)
    print(f"{'MINI HOJA DE CÁLCULO ACADÉMICA':^75}")
    print("="*75)
    print(f"{'Código':<12}{'Nombre Completo':<30}{'N1':<8}{'N2':<8}{'N3':<8}{'Promedio':<10}")
    print("-"*75)
    for e in hoja:
        print(f"{e['codigo']:<12}{e['nombre']:<30}{e['nota1']:<8.1f}{e['nota2']:<8.1f}{e['nota3']:<8.1f}{e['promedio']:<10.2f}")
    print("="*75)

def buscar_estudiante():
    codigo = input("\nIngrese código a buscar en la estructura asociativa: ").strip()
    if codigo in indice_hash:
        pos = indice_hash[codigo]
        e = hoja[pos]
        print(f"\n[ENCONTRADO O(1)] {e['nombre']} | Promedio Evaluado: {e['promedio']:.2f}")
    else:
        print("[AVISO] El código buscado no existe en la base indexada.")

def quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[-1]
    # Clasificación de Mayor a Menor (Descendente por Promedio)
    mayores = [x for x in lista[:-1] if x["promedio"] >= pivote["promedio"]]
    menores = [x for x in lista[:-1] if x["promedio"] < pivote["promedio"]]
    return quicksort(mayores) + [pivote] + quicksort(menores)

def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    return merge(izquierda, derecha)

def merge(izquierda, derecha):
    resultado = []
    i = j = 0
    # Clasificación de Menor a Mayor alfanumérico (Ascendente por Código)
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i]["codigo"] <= derecha[j]["codigo"]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

def ordenar_por_promedio():
    global hoja
    if not hoja: 
        print("[AVISO] No hay estudiantes para ordenar.")
        return
    guardar_historial()
    hoja = quicksort(hoja)
    actualizar_hash()
    print("[OK] Matriz ordenada por Promedio vía QuickSort Funcional.")

def ordenar_por_codigo():
    global hoja
    if not hoja: 
        print("[AVISO] No hay estudiantes para ordenar.")
        return
    guardar_historial()
    hoja = merge_sort(hoja)
    actualizar_hash()
    print("[OK] Matriz ordenada por Código vía MergeSort Estable.")

def deshacer():
    global hoja
    if historial:
        hoja = historial.pop()
        actualizar_hash()
        print("[REVERSIÓN] Estado de memoria restaurado a la versión previa.")
    else:
        print("[INFO] El historial de modificaciones está vacío.")

def agregar_cola_atencion():
    codigo = input("\nIngrese código del estudiante en espera: ").strip()
    if codigo in indice_hash:
        cola_atencion.append(codigo)
        print("[COLA] Estudiante insertado en la cola FIFO institucional.")
    else:
        print("[ERROR] Código no registrado en las celdas vigentes.")

def atender_estudiante():
    if cola_atencion:
        codigo = cola_atencion.popleft()
        if codigo in indice_hash:
            pos = indice_hash[codigo]
            print(f"[ATENCIÓN] Despachando requerimiento de: {hoja[pos]['nombre']}")
        else:
            print("[AVISO] El estudiante en cola ya no se encuentra en los registros activos.")
    else:
        print("[INFO] No se registran estudiantes pendientes en la cola.")

def suma_promedios_recursiva(i):
    """Mantenida por requerimiento de diseño recursivo (aplica para colecciones pequeñas)."""
    if i == len(hoja):
        return 0.0
    return hoja[i]["promedio"] + suma_promedios_recursiva(i + 1)

def estadisticas():
    if not hoja:
        print("[AVISO] Datos insuficientes para el análisis.")
        return
    
    # Cálculo recursivo del promedio general solicitado
    try:
        suma = suma_promedios_recursiva(0)
    except RecursionError:
        # Salvaguarda iterativa si excede el límite de recursión de Python
        suma = sum(e["promedio"] for e in hoja)
        
    promedio_general = suma / len(hoja)
    
    # Analítica extra añadida para mejorar la función
    max_estudiante = max(hoja, key=lambda x: x["promedio"])
    min_estudiante = min(hoja, key=lambda x: x["promedio"])

    print("\n" + "="*50)
    print(f"{'ANALÍTICA Y ESTADÍSTICAS GENERALES':^50}")
    print("="*50)
    print(f" Estudiantes Registrados  : {len(hoja)}")
    print(f" Promedio General Cohorte : {promedio_general:.2f}")
    print(f" Promedio Más Alto        : {max_estudiante['promedio']:.2f} ({max_estudiante['nombre']})")
    print(f" Promedio Más Bajo        : {min_estudiante['promedio']:.2f} ({min_estudiante['nombre']})")
    print(f" Estudiantes en Cola      : {len(cola_atencion)}")
    print("="*50)

def menu():
    while True:
        print("\n" + "="*45)
        print("     MENU PRINCIPAL - PYTHON CORE SYSTEMS    ")
        print("="*45)
        print("1. Registrar estudiante (Fila)")
        print("2. Mostrar hoja de cálculo")
        print("3. Buscar estudiante por código (Hash)")
        print("4. Ordenar por promedio (QuickSort)")
        print("5. Ordenar por código (MergeSort)")
        print("6. Deshacer última acción (Stack)")
        print("7. Agregar a cola de espera (Queue)")
        print("8. Atender siguiente estudiante (FIFO)")
        print("9. Analítica y Estadísticas generales")
        print("10. Salir del programa")
        print("-" * 45)
        
        opcion = input("Seleccione una opción (1-10): ").strip()
        if opcion == "1": registrar_estudiante()
        elif opcion == "2": mostrar_hoja()
        elif opcion == "3": buscar_estudiante()
        elif opcion == "4": ordenar_por_promedio()
        elif opcion == "5": ordenar_por_codigo()
        elif opcion == "6": deshacer()
        elif opcion == "7": agregar_cola_atencion()
        elif opcion == "8": atender_estudiante()
        elif opcion == "9": estadisticas()
        elif opcion == "10":
            print("Finalizando subprocesos interpretados... Salida.")
            break
        else:
            print("[ERROR] Código numérico no asignado en el menú.")

if __name__ == "__main__":
    menu()